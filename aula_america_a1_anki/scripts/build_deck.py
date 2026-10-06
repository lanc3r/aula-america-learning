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
    commands = [
        [sys.executable, str(ROOT / "scripts" / "validate_content.py")],
        [sys.executable, str(ROOT / "scripts" / "audit_card_design.py")],
    ]

    for command in commands:
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

def tts_for_profile(tts: dict[str, Any], profile: str) -> dict[str, Any]:
    effective = dict(tts)
    profiles = tts.get("profiles", {})
    if profile != "default":
        if not isinstance(profiles, dict) or profile not in profiles:
            raise ValueError(f"未知 TTS profile：{profile}")
        spec = profiles[profile]
        if not isinstance(spec, dict):
            raise ValueError(f"TTS profile 必须是对象：{profile}")
        if "speed" in spec:
            effective["speed"] = spec["speed"]
        profile_instructions = str(spec.get("instructions", "")).strip()
        if profile_instructions:
            base = str(effective.get("instructions", "")).strip()
            effective["instructions"] = "\n\n".join(
                part for part in (base, profile_instructions) if part
            )
    return effective

def instructions_for(text: str, tts: dict[str, Any]) -> str:
    base = str(tts.get("instructions", "")).strip()
    overrides = tts.get("text_instruction_overrides", {})
    if not isinstance(overrides, dict):
        raise ValueError(
            "tts_config.json 中的 text_instruction_overrides 必须是对象。"
        )
    extra = str(overrides.get(text, "")).strip()
    return "\n\n".join(part for part in (base, extra) if part)

def audio_key(text: str, tts: dict[str, Any], profile: str = "default") -> str:
    effective = tts_for_profile(tts, profile)
    payload = "\n".join([
        effective["model"],
        effective["voice"],
        str(effective["speed"]),
        profile,
        instructions_for(text, effective),
        text
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:18]

def audio_path_for(
    text: str,
    tts: dict[str, Any],
    profile: str = "default"
) -> Path:
    effective = tts_for_profile(tts, profile)
    return CACHE_DIR / (
        f'{effective["cache_prefix"]}_{audio_key(text, tts, profile)}.'
        f'{effective["response_format"]}'
    )

def collect_content(note_types: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    collected = {key: [] for key in note_types["note_types"]}
    for path in sorted(CONTENT_DIR.glob("unidad_*.json")):
        data = load_json(path)
        for type_name in collected:
            collected[type_name].extend(data["cards"].get(type_name, []))
    return collected

def collect_audio_requests(
    collected: dict[str, list[dict[str, Any]]],
    note_types: dict[str, Any]
) -> list[tuple[str, str]]:
    requests: set[tuple[str, str]] = set()
    for type_name, cards in collected.items():
        spec = note_types["note_types"][type_name]
        fields = spec["audio_content_fields"]
        profile = str(spec.get("audio_profile", "default"))
        for card in cards:
            for field in fields:
                value = str(card.get(field, "")).strip()
                if value:
                    requests.add((profile, value))
    return sorted(requests)

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
    refresh: bool,
    profile: str = "default"
) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    effective = tts_for_profile(tts, profile)
    out_path = audio_path_for(text, tts, profile)

    if out_path.exists() and out_path.stat().st_size > 1000 and not refresh:
        print(f"  使用缓存：{text}")
        return out_path

    print(f"  生成音频：{text}")
    last_error: Exception | None = None

    for attempt in range(1, 4):
        try:
            with client.audio.speech.with_streaming_response.create(
                model=effective["model"],
                voice=effective["voice"],
                input=text,
                instructions=instructions_for(text, effective),
                response_format=effective["response_format"],
                speed=effective["speed"],
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
    requests: list[tuple[str, str]],
    tts: dict[str, Any],
    refresh: bool
) -> dict[tuple[str, str], Path]:
    missing = [
        (profile, text) for profile, text in requests
        if refresh
        or not audio_path_for(text, tts, profile).exists()
        or audio_path_for(text, tts, profile).stat().st_size <= 1000
    ]

    client = None
    if missing:
        print(f"有 {len(missing)} 条音频需要生成。")
        client = get_api_client()
    else:
        print("全部音频已存在，将直接复用缓存。")

    audio_map: dict[tuple[str, str], Path] = {}
    for index, (profile, text) in enumerate(requests, start=1):
        print(f"[{index}/{len(requests)}] [{profile}]")
        if client is None:
            path = audio_path_for(text, tts, profile)
            print(f"  使用缓存：{text}")
        else:
            path = generate_audio(client, text, tts, refresh, profile)
        audio_map[(profile, text)] = path
    return audio_map

def sound_field(
    text: str,
    audio_map: dict[tuple[str, str], Path],
    profile: str = "default"
) -> str:
    if not text:
        return ""
    return f"[sound:{audio_map[(profile, text)].name}]"

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
    audio_map: dict[tuple[str, str], Path],
    note_types: dict[str, Any]
) -> list[str]:
    profile = str(
        note_types["note_types"][type_name].get("audio_profile", "default")
    )
    if type_name == "chunk_production":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["context_zh"], card["prompt_zh"], card["spanish"],
            card["meaning_zh"], sound_field(card["spanish"], audio_map, profile),
            card["usage_zh"], card["pattern"], card["note"]
        ]
    if type_name == "dialogue_response":
        return [
            card["uid"], card["unit"], card["lesson"], card["context_zh"],
            card["question_es"],
            sound_field(card["question_es"], audio_map, profile),
            card["answer_es"], card["answer_zh"],
            sound_field(card["answer_es"], audio_map, profile),
            card["usage_zh"]
        ]
    if type_name == "mistake_contrast":
        return [
            card["uid"], card["unit"], card["lesson"], card["context_zh"],
            card["prompt_zh"], card["wrong_es"], card["correct_es"],
            sound_field(card["correct_es"], audio_map, profile),
            card["explanation_zh"]
        ]
    if type_name == "vocabulary":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["prompt_zh"], card["word_es"], card["gender"],
            card["plural_es"], card["meaning_zh"],
            sound_field(card["word_es"], audio_map, profile),
            card["example_es"], card["example_zh"],
            sound_field(card["example_es"], audio_map, profile),
            card["usage_zh"], card["regional_variant"]
        ]
    if type_name == "grammar_pattern":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["context_zh"], card["prompt_zh"], card["answer_es"],
            sound_field(card["answer_es"], audio_map, profile),
            card["meaning_zh"], card["pattern"],
            card["explanation_zh"],
            (
                card["contrast_es"]
                + ("<br>" + sound_field(card["contrast_es"], audio_map, profile)
                   if card["contrast_es"] else "")
            ),
            card["note"]
        ]
    if type_name == "rule_concept":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["question_zh"], card["core_answer_zh"], card["example_es"],
            sound_field(card["example_es"], audio_map, profile),
            card["explanation_zh"], card["english_comparison"],
            card["japanese_comparison"], card["negative_transfer"],
            card["note"]
        ]
    if type_name == "pronunciation":
        return [
            card["uid"], card["unit"], card["lesson"], card["category"],
            card["task_zh"], card["target_es"],
            sound_field(card["target_es"], audio_map, profile),
            card["contrast_es"],
            sound_field(card["contrast_es"], audio_map, profile),
            card["articulation_zh"], card["common_error_zh"],
            card["practice_cue_zh"], card["note"]
        ]
    if type_name == "listening_dialogue":
        return [
            card["uid"], card["unit"], card["lesson"], card["context_zh"],
            card["task_zh"], card["transcript_es"],
            sound_field(card["transcript_es"], audio_map, profile),
            card["meaning_zh"], card["listening_focus_zh"], card["note"]
        ]
    raise ValueError(f"未知卡片类型：{type_name}")

def build_deck(
    deck_config: dict[str, Any],
    note_types: dict[str, Any],
    collected: dict[str, list[dict[str, Any]]],
    audio_map: dict[tuple[str, str], Path]
) -> Path:
    genanki = import_dependencies()
    models = make_models(genanki, note_types)
    deck = genanki.Deck(deck_config["deck_id"], deck_config["deck_name"])

    ordered_cards = []
    for type_name, cards in collected.items():
        for card in cards:
            ordered_cards.append((card.get("learning_order", 999999999), type_name, card))
    ordered_cards.sort(key=lambda x: (x[0], x[2]["uid"]))
    for _, type_name, card in ordered_cards:
        model = models[type_name]
        note = genanki.Note(model=model, fields=map_fields(type_name, card, audio_map, note_types), tags=card["tags"])
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
    audio_map: dict[tuple[str, str], Path]
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
                    or card.get("transcript_es")
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
    requests = collect_audio_requests(collected, note_types)

    print()
    print(f"需要 {len(requests)} 条唯一音频请求。")
    audio_map = build_audio_map(requests, tts, args.refresh_audio)
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
