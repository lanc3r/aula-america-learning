from __future__ import annotations

import argparse
import csv
import getpass
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
CONTENT_DIR = ROOT / "content"
TEMPLATE_DIR = ROOT / "templates"
CACHE_DIR = ROOT / "audio_cache"
OUTPUT_DIR = ROOT / "output"
RELEASE_DIR = ROOT / "release"

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")

def run_validation() -> None:
    command = [sys.executable, str(ROOT / "scripts" / "validate_content.py")]
    result = subprocess.run(command)

    if result.returncode != 0:
        raise SystemExit(
            "\n内容验证失败，已停止生成。"
            "\n请根据上方列出的具体项目修正后重试。"
        )

def import_dependencies():
    try:
        import genanki
    except ImportError as exc:
        raise SystemExit(
            "缺少 genanki。请通过 build_deck.command 启动，"
            "它会在独立环境中自动安装依赖。"
        ) from exc
    return genanki

def audio_key(text: str, tts: dict[str, Any]) -> str:
    payload = "\n".join([
        tts["model"],
        tts["voice"],
        str(tts["speed"]),
        tts["instructions"],
        text
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:18]

def audio_path_for(text: str, tts: dict[str, Any]) -> Path:
    return CACHE_DIR / (
        f'{tts["cache_prefix"]}_{audio_key(text, tts)}.'
        f'{tts["response_format"]}'
    )

def collect_content(note_types: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    collected = {key: [] for key in note_types["note_types"]}
    for path in sorted(CONTENT_DIR.glob("unidad_*.json")):
        data = load_json(path)
        for type_name in collected:
            collected[type_name].extend(data["cards"].get(type_name, []))
    return collected

def collect_audio_texts(
    collected: dict[str, list[dict[str, Any]]],
    note_types: dict[str, Any]
) -> list[str]:
    texts: set[str] = set()
    for type_name, cards in collected.items():
        fields = note_types["note_types"][type_name]["audio_content_fields"]
        for card in cards:
            for field in fields:
                value = str(card.get(field, "")).strip()
                if value:
                    texts.add(value)
    return sorted(texts)

def get_api_client():
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit(
            "缺少 openai。请通过 build_deck.command 启动，"
            "它会在独立环境中自动安装依赖。"
        ) from exc

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        api_key = getpass.getpass(
            "请输入 OpenAI API key（输入不会显示，也不会写入文件）："
        ).strip()
    if not api_key:
        raise SystemExit("没有提供 API key，已停止。")
    return OpenAI(api_key=api_key)

def generate_audio(
    client,
    text: str,
    tts: dict[str, Any],
    refresh: bool
) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    out_path = audio_path_for(text, tts)

    if out_path.exists() and out_path.stat().st_size > 1000 and not refresh:
        print(f"  使用缓存：{text}")
        return out_path

    print(f"  生成音频：{text}")
    last_error: Exception | None = None

    for attempt in range(1, 4):
        try:
            with client.audio.speech.with_streaming_response.create(
                model=tts["model"],
                voice=tts["voice"],
                input=text,
                instructions=tts["instructions"],
                response_format=tts["response_format"],
                speed=tts["speed"],
            ) as response:
                response.stream_to_file(out_path)

            if out_path.exists() and out_path.stat().st_size > 1000:
                return out_path
            raise RuntimeError("API 返回的音频文件为空或异常。")
        except Exception as exc:
            last_error = exc
            if out_path.exists():
                out_path.unlink()
            if attempt < 3:
                wait = 2 ** attempt
                print(f"    第 {attempt} 次失败，{wait} 秒后重试……")
                time.sleep(wait)

    raise RuntimeError(f"生成失败：{text}\n{last_error}") from last_error

def build_audio_map(
    texts: list[str],
    tts: dict[str, Any],
    refresh: bool
) -> dict[str, Path]:
    missing = [
        text for text in texts
        if refresh
        or not audio_path_for(text, tts).exists()
        or audio_path_for(text, tts).stat().st_size <= 1000
    ]

    client = None
    if missing:
        print(f"有 {len(missing)} 条音频需要生成。")
        client = get_api_client()
    else:
        print("全部音频已存在，将直接复用缓存。")

    audio_map: dict[str, Path] = {}
    for index, text in enumerate(texts, start=1):
        print(f"[{index}/{len(texts)}]")
        if client is None:
            path = audio_path_for(text, tts)
            print(f"  使用缓存：{text}")
        else:
            path = generate_audio(client, text, tts, refresh)
        audio_map[text] = path
    return audio_map

def sound_field(text: str, audio_map: dict[str, Path]) -> str:
    if not text:
        return ""
    return f"[sound:{audio_map[text].name}]"

def make_models(genanki, note_types: dict[str, Any]):
    models = {}
    for type_name, spec in note_types["note_types"].items():
        models[type_name] = genanki.Model(
            spec["model_id"],
            spec["model_name"],
            fields=[{"name": field} for field in spec["fields"]],
            templates=[{
                "name": spec["template_name"],
                "qfmt": read_text(spec["front_template"]),
                "afmt": read_text(spec["back_template"])
            }],
            css=read_text(spec["style_file"])
        )
    return models

def map_fields(
    type_name: str,
    card: dict[str, Any],
    audio_map: dict[str, Path]
) -> list[str]:
    if type_name == "chunk_production":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["context_zh"], card["prompt_zh"], card["spanish"],
            card["meaning_zh"], sound_field(card["spanish"], audio_map),
            card["usage_zh"], card["pattern"], card["note"]
        ]
    if type_name == "dialogue_response":
        return [
            card["uid"], card["unit"], card["lesson"], card["context_zh"],
            card["question_es"],
            sound_field(card["question_es"], audio_map),
            card["answer_es"], card["answer_zh"],
            sound_field(card["answer_es"], audio_map),
            card["usage_zh"]
        ]
    if type_name == "mistake_contrast":
        return [
            card["uid"], card["unit"], card["lesson"], card["context_zh"],
            card["prompt_zh"], card["wrong_es"], card["correct_es"],
            sound_field(card["correct_es"], audio_map),
            card["explanation_zh"]
        ]
    if type_name == "vocabulary":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["prompt_zh"], card["word_es"], card["gender"],
            card["plural_es"], card["meaning_zh"],
            sound_field(card["word_es"], audio_map),
            card["example_es"], card["example_zh"],
            sound_field(card["example_es"], audio_map),
            card["usage_zh"], card["regional_variant"]
        ]
    if type_name == "grammar_pattern":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["context_zh"], card["prompt_zh"], card["answer_es"],
            sound_field(card["answer_es"], audio_map),
            card["meaning_zh"], card["pattern"],
            card["explanation_zh"], card["contrast_es"], card["note"]
        ]
    if type_name == "rule_concept":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["question_zh"], card["core_answer_zh"], card["example_es"],
            sound_field(card["example_es"], audio_map),
            card["explanation_zh"], card["english_comparison"],
            card["japanese_comparison"], card["negative_transfer"],
            card["note"]
        ]
    if type_name == "pronunciation":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["task_zh"], card["target_es"],
            sound_field(card["target_es"], audio_map),
            card["contrast_es"],
            sound_field(card["contrast_es"], audio_map),
            card["articulation_zh"], card["common_error_zh"],
            card["practice_cue_zh"], card["note"]
        ]
    raise ValueError(f"未知卡片类型：{type_name}")

def build_deck(
    deck_config: dict[str, Any],
    note_types: dict[str, Any],
    collected: dict[str, list[dict[str, Any]]],
    audio_map: dict[str, Path]
) -> Path:
    genanki = import_dependencies()
    models = make_models(genanki, note_types)
    deck = genanki.Deck(deck_config["deck_id"], deck_config["deck_name"])

    for type_name, cards in collected.items():
        model = models[type_name]
        for card in cards:
            note = genanki.Note(
                model=model,
                fields=map_fields(type_name, card, audio_map),
                tags=card["tags"]
            )
            note.guid = genanki.guid_for(card["uid"])
            deck.add_note(note)

    OUTPUT_DIR.mkdir(exist_ok=True)
    RELEASE_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / deck_config["output_file"]
    release_path = RELEASE_DIR / deck_config["output_file"]

    package = genanki.Package(deck)
    package.media_files = [
        str(path) for path in sorted(set(audio_map.values()))
    ]
    package.write_to_file(str(output_path))
    package.write_to_file(str(release_path))
    return output_path

def export_manifest(
    deck_config: dict[str, Any],
    collected: dict[str, list[dict[str, Any]]],
    audio_map: dict[str, Path]
) -> Path:
    manifest_path = RELEASE_DIR / "release_manifest.json"
    counts = {key: len(value) for key, value in collected.items()}
    manifest = {
        "version": deck_config["version"],
        "deck_file": deck_config["output_file"],
        "deck_name": deck_config["deck_name"],
        "card_counts": counts,
        "total_cards": sum(counts.values()),
        "unique_audio_files": len(set(audio_map.values())),
        "contract_hash": deck_config["contract_hash"]
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return manifest_path

def export_content_tsv(
    collected: dict[str, list[dict[str, Any]]]
) -> Path:
    path = RELEASE_DIR / "content_summary.tsv"
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(["uid", "type", "primary_spanish", "tags"])
        for type_name, cards in collected.items():
            for card in cards:
                primary = (
                    card.get("spanish")
                    or card.get("question_es")
                    or card.get("correct_es")
                    or card.get("word_es")
                    or card.get("answer_es")
                    or card.get("example_es")
                    or card.get("target_es")
                    or ""
                )
                writer.writerow([
                    card["uid"], type_name, primary,
                    " ".join(card["tags"])
                ])
    return path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh_audio", action="store_true")
    args = parser.parse_args()

    run_validation()

    deck_config = load_json(CONFIG_DIR / "deck_config.json")
    tts = load_json(CONFIG_DIR / "tts_config.json")
    note_types = load_json(CONFIG_DIR / "note_types.json")
    collected = collect_content(note_types)
    texts = collect_audio_texts(collected, note_types)

    print()
    print(f"需要 {len(texts)} 条唯一音频。")
    audio_map = build_audio_map(texts, tts, args.refresh_audio)
    output_path = build_deck(
        deck_config, note_types, collected, audio_map
    )
    manifest_path = export_manifest(deck_config, collected, audio_map)
    summary_path = export_content_tsv(collected)

    print()
    print("生成完成")
    print("--------")
    print(f"牌组：{output_path}")
    print(f"发布清单：{manifest_path}")
    print(f"内容摘要：{summary_path}")

if __name__ == "__main__":
    main()
