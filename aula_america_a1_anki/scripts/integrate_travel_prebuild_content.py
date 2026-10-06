#!/usr/bin/env python3
"""Convert travel prebuild TSV files into the repository content schema."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
PREBUILDS_DIR = ROOT / "prebuilds"


SOURCES = [
    {
        "unit": "NVH-U6",
        "title": "Por la ciudad",
        "lesson_prefix": "U6",
        "path": PREBUILDS_DIR / "v047" / "anki_v047_nvh_u6_prebuild.tsv",
        "output": CONTENT_DIR / "unidad_nvh_06.json",
        "source_tag": "source::v047_prebuild",
        "order_base": 760000,
    },
    {
        "unit": "NVH-U7",
        "title": "El placer de viajar",
        "lesson_prefix": "U7",
        "path": PREBUILDS_DIR / "v048_v050" / "anki_v048_nvh_u7_prebuild.tsv",
        "output": CONTENT_DIR / "unidad_nvh_07.json",
        "source_tag": "source::v048_prebuild",
        "order_base": 770000,
    },
    {
        "unit": "NVH-U8",
        "title": "Mirador review",
        "lesson_prefix": "U8",
        "path": PREBUILDS_DIR / "v048_v050" / "anki_v049_nvh_u8_mirador_review.tsv",
        "output": CONTENT_DIR / "unidad_nvh_08.json",
        "source_tag": "source::v049_mirador_review",
        "order_base": 780000,
    },
    {
        "unit": "NVH-U9",
        "title": "Caminando",
        "lesson_prefix": "U9",
        "path": PREBUILDS_DIR / "v048_v050" / "anki_v050_nvh_u9_prebuild.tsv",
        "output": CONTENT_DIR / "unidad_nvh_09.json",
        "source_tag": "source::v050_prebuild",
        "order_base": 790000,
    },
]


GROUP_ORDER = {
    "vocab": "01_基础词汇",
    "lexico": "01_基础词汇",
    "grammar": "04_语法模式",
    "phrase": "05_高频句块",
    "sentence": "05_高频句块",
    "review_phrase": "05_高频句块",
    "qa": "06_问答情景",
    "dialogue": "06_问答情景",
    "contrast": "07_易错综合",
    "error_review": "07_易错综合",
    "micro_output": "08_小段输出",
}


def tags_from(row: dict[str, str], source_tag: str) -> list[str]:
    raw = [tag for tag in row["tags"].split() if tag]
    normalized = []
    for tag in raw:
        if "::" in tag:
            normalized.append(tag)
        else:
            normalized.append(tag.replace("-", "_"))
    normalized.append(source_tag)
    return list(dict.fromkeys(normalized))


def lesson_from(tags: list[str], lesson_prefix: str) -> str:
    for tag in tags:
        match = re.search(r"(?:u\d+_block_|u\d+_review_)(\d+)", tag)
        if match:
            return f"L{int(match.group(1)):02d}"
    return "L01"


def learning_group(tags: list[str]) -> str:
    for tag in tags:
        if tag in GROUP_ORDER:
            return GROUP_ORDER[tag]
    return "05_高频句块"


def gender_and_plural(spanish: str) -> tuple[str, str]:
    parts = spanish.split(maxsplit=1)
    if len(parts) != 2:
        return "", ""
    article, noun = parts
    if article == "el":
        return "m.", "los " + pluralize(noun)
    if article == "la":
        return "f.", "las " + pluralize(noun)
    if article == "los":
        return "m. pl.", spanish
    if article == "las":
        return "f. pl.", spanish
    return "", ""


def pluralize(noun: str) -> str:
    if not noun:
        return noun
    head, *tail = noun.split()
    if head.endswith(("s", "x")):
        plural = head
    elif head[-1].lower() in "aeiouáéíóú":
        plural = head + "s"
    else:
        plural = head + "es"
    return " ".join([plural, *tail])


def looks_like_question(text: str) -> bool:
    return text.startswith("¿") or text.endswith("?")


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def clean_audio_spanish(text: str) -> str:
    """Keep audio fields Spanish-only and aligned with the repo validator."""
    value = text.strip()
    if "：" in value and ("¿" in value or "¡" in value):
        value = value.split("：", 1)[1].strip()
    if value.endswith("?") and not value.startswith("¿"):
        value = "¿" + value.replace("¿", "", 1)
    if value.endswith("!") and not value.startswith("¡"):
        value = "¡" + value.replace("¡", "", 1)
    return value


def card_type(row: dict[str, str], tags: list[str]) -> str:
    back = row["back"].strip()
    front = row["front"].strip()
    if "vocab" in tags or "lexico" in tags or "连冠词" in front:
        return "vocabulary"
    if "contrast" in tags or "error_review" in tags or front.startswith("改错"):
        return "mistake_contrast"
    if "grammar" in tags or "verb" in tags or "reflexive" in tags or "gerund" in tags:
        return "grammar_pattern"
    if "qa" in tags or "dialogue" in tags:
        return "dialogue_response"
    if looks_like_question(front) and not has_cjk(front):
        return "dialogue_response"
    return "chunk_production"


def make_uid(unit: str, lesson: str, type_name: str, seq: int) -> str:
    prefix = {
        "chunk_production": "P",
        "dialogue_response": "D",
        "mistake_contrast": "M",
        "vocabulary": "V",
        "grammar_pattern": "G",
        "rule_concept": "R",
        "pronunciation": "PR",
    }[type_name]
    return f"{unit}-{lesson}-{prefix}{seq:03d}"


def make_card(
    row: dict[str, str],
    meta: dict[str, object],
    type_name: str,
    lesson: str,
    seq: int,
    order: int,
    tags: list[str],
) -> dict[str, object]:
    front = row["front"].strip()
    back = clean_audio_spanish(row["back"].strip())
    extra = row.get("extra", "").strip()
    group = learning_group(tags)
    base = {
        "uid": make_uid(str(meta["unit"]), lesson, type_name, seq),
        "unit": meta["unit"],
        "lesson": lesson,
        "tags": tags + [f"group::{group}"],
        "learning_group": group,
        "learning_order": order,
    }

    if type_name == "vocabulary":
        gender, plural = gender_and_plural(back)
        return {
            **base,
            "category": "旅行预装词汇",
            "prompt_zh": front.replace("；连冠词", ""),
            "word_es": back,
            "gender": gender,
            "plural_es": plural,
            "meaning_zh": front.replace("；连冠词", ""),
            "example_es": "",
            "example_zh": "",
            "usage_zh": extra,
            "regional_variant": "LatAm/MX supplement" if "latam" in tags or "mexico" in tags else "",
        }

    if type_name == "grammar_pattern":
        return {
            **base,
            "category": "旅行预装语法",
            "context_zh": "旅行/日常课堂顺序",
            "prompt_zh": front,
            "answer_es": back,
            "meaning_zh": front,
            "pattern": "",
            "explanation_zh": extra,
            "contrast_es": "",
            "note": "",
        }

    if type_name == "dialogue_response":
        if looks_like_question(back):
            question_es = back
            answer_es = ""
            answer_zh = front
        else:
            question_es = front if looks_like_question(front) else ""
            answer_es = back
            answer_zh = front
        return {
            **base,
            "context_zh": "旅行/日常问答",
            "question_es": question_es,
            "answer_es": answer_es,
            "answer_zh": answer_zh,
            "usage_zh": extra,
        }

    if type_name == "mistake_contrast":
        wrong = ""
        if "：" in front:
            wrong = front.split("：", 1)[1].strip()
        return {
            **base,
            "context_zh": "旅行/日常易错辨析",
            "prompt_zh": front,
            "wrong_es": wrong,
            "correct_es": back,
            "explanation_zh": extra,
        }

    return {
        **base,
        "category": "旅行预装句块",
        "context_zh": "旅行/日常课堂顺序",
        "prompt_zh": front,
        "spanish": back,
        "meaning_zh": front,
        "usage_zh": extra,
        "pattern": "",
        "note": "",
    }


def convert_source(meta: dict[str, object]) -> dict[str, object]:
    source_path = Path(meta["path"])
    buckets: dict[str, list[dict[str, object]]] = defaultdict(list)
    counters: dict[tuple[str, str], int] = defaultdict(int)

    with source_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        for index, row in enumerate(reader, start=1):
            tags = tags_from(row, str(meta["source_tag"]))
            lesson = lesson_from(tags, str(meta["lesson_prefix"]))
            type_name = card_type(row, tags)
            counters[(lesson, type_name)] += 1
            card = make_card(
                row,
                meta,
                type_name,
                lesson,
                counters[(lesson, type_name)],
                int(meta["order_base"]) + index,
                tags,
            )
            buckets[type_name].append(card)

    return {
        "unit": meta["unit"],
        "title": meta["title"],
        "status": "prebuild_integrated",
        "content_version": "0.5.4",
        "cards": {key: buckets.get(key, []) for key in [
            "chunk_production",
            "dialogue_response",
            "mistake_contrast",
            "vocabulary",
            "grammar_pattern",
            "rule_concept",
            "pronunciation",
        ]},
    }


def main() -> None:
    for meta in SOURCES:
        data = convert_source(meta)
        output = Path(meta["output"])
        output.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        total = sum(len(v) for v in data["cards"].values())
        print(f"{output.relative_to(ROOT)}: {total} cards")


if __name__ == "__main__":
    main()
