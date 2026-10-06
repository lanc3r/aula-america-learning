from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
CONTENT_DIR = ROOT / "content"
MAX_WARNINGS_TO_PRINT = 20

CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
SPANISH_SENTENCE_END_RE = re.compile(r"[.!?。！？]")
INTERNAL_METADATA_RE = re.compile(
    r"\b(Replaces retired|retired pseudo|retired UID|NVH-[A-Z0-9-]+-[A-Z]\d+)\b"
)
LEARNER_VISIBLE_FIELDS = {
    "category",
    "context_zh",
    "prompt_zh",
    "meaning_zh",
    "usage_zh",
    "pattern",
    "note",
    "explanation_zh",
    "core_answer_zh",
    "example_zh",
}
REUSABLE_CHUNK_PATTERNS = [
    (re.compile(r"^¿Sabe si\b", re.IGNORECASE), "¿Sabe si ...?"),
    (re.compile(r"^¿Hay\b", re.IGNORECASE), "¿Hay ...?"),
    (re.compile(r"^Hay\b"), "Hay + 名词"),
    (re.compile(r"^No hay\b", re.IGNORECASE), "No hay + 名词"),
    (re.compile(r"^¿Dónde está\b", re.IGNORECASE), "¿Dónde está ...?"),
    (re.compile(r"^Disculpe, ¿dónde está\b", re.IGNORECASE), "Disculpe, ¿dónde está ...?"),
    (re.compile(r"^Disculpe, ¿cómo llego\b", re.IGNORECASE), "Disculpe, ¿cómo llego a ...?"),
    (re.compile(r"^¿Me puede recomendar\b", re.IGNORECASE), "¿Me puede recomendar ...?"),
    (re.compile(r"^¿Tiene\b", re.IGNORECASE), "¿Tiene ...?"),
    (re.compile(r"^¿A qué hora\b", re.IGNORECASE), "¿A qué hora ...?"),
    (re.compile(r"^¿.+ está abiert[oa]\?", re.IGNORECASE), "¿... está abierto/a?"),
    (re.compile(r"^¿Dónde se pueden?\b", re.IGNORECASE), "¿Dónde se puede(n) ...?"),
    (re.compile(r"^¿Cuánto cuesta\b", re.IGNORECASE), "¿Cuánto cuesta ...?"),
    (re.compile(r"^¿De dónde sale\b", re.IGNORECASE), "¿De dónde sale ...?"),
    (re.compile(r"^¿Tengo que\b", re.IGNORECASE), "¿Tengo que ...?"),
    (re.compile(r"^Tengo que\b"), "Tengo que + infinitivo"),
    (re.compile(r"^Tiene que\b"), "Tiene que + infinitivo"),
    (re.compile(r"^¿Puedo ir\b", re.IGNORECASE), "¿Puedo ir ...?"),
    (re.compile(r"^¿Est[ae] .+ va a", re.IGNORECASE), "¿Este/Esta ... va a ...?"),
    (re.compile(r"^¿Qué línea tengo que tomar\b", re.IGNORECASE), "¿Qué línea tengo que tomar ...?"),
    (re.compile(r"^¿Dónde tengo que\b", re.IGNORECASE), "¿Dónde tengo que ...?"),
    (re.compile(r"^¿Cuánt[oa]s? .+ son\?", re.IGNORECASE), "¿Cuántos/as ... son?"),
    (re.compile(r"^¿Es\b", re.IGNORECASE), "¿Es ...?"),
    (re.compile(r"¿verdad\?$", re.IGNORECASE), "..., ¿verdad?"),
    (re.compile(r"^¿Cuánto se tarda\?", re.IGNORECASE), "¿Cuánto se tarda?"),
    (re.compile(r"^Es mejor\b"), "Es mejor + infinitivo"),
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def location(path: Path, type_name: str, index: int, card: dict[str, Any]) -> str:
    uid = str(card.get("uid", "")).strip() or f"#{index}"
    return f"{path.name}:{type_name}[{index}] {uid}"


def count_sentences(text: str) -> int:
    return len([part for part in SPANISH_SENTENCE_END_RE.split(text) if part.strip()])


def audit_file(path: Path, note_types: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    data = load_json(path)
    cards = data.get("cards", {})
    prompt_targets: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)

    total_cards = sum(len(entries) for entries in cards.values() if isinstance(entries, list))
    lessons = {
        str(card.get("lesson", "")).strip()
        for entries in cards.values()
        if isinstance(entries, list)
        for card in entries
        if str(card.get("lesson", "")).strip()
    }
    if total_cards >= 40 and len(lessons) <= 1:
        errors.append(
            f"{path.name}: {total_cards} cards are assigned to only one lesson; "
            "split the unit into lesson blocks."
        )

    for type_name, spec in note_types["note_types"].items():
        entries = cards.get(type_name, [])
        if not isinstance(entries, list):
            continue

        audio_fields = spec.get("audio_content_fields", [])
        for index, card in enumerate(entries, start=1):
            loc = location(path, type_name, index, card)

            for field in LEARNER_VISIBLE_FIELDS:
                value = str(card.get(field, "")).strip()
                if value and INTERNAL_METADATA_RE.search(value):
                    errors.append(
                        f"{loc}: learner-visible field contains internal metadata: "
                        f"{field}={value}"
                    )

            for field in audio_fields:
                value = str(card.get(field, "")).strip()
                if not value:
                    continue
                if CHINESE_RE.search(value):
                    errors.append(f"{loc}: audio field contains Chinese: {field}={value}")
                if " / " in value and field in {"spanish", "question_es", "answer_es", "correct_es", "answer_es", "target_es"}:
                    errors.append(
                        f"{loc}: main audio field has slash-separated alternatives; "
                        f"keep one main answer and move variants to usage/note: {field}={value}"
                    )
                elif " / " in value:
                    warnings.append(
                        f"{loc}: supporting audio field has slash-separated alternatives; "
                        f"review when this card is next edited: {field}={value}"
                    )

            if type_name == "chunk_production":
                prompt = str(card.get("prompt_zh", "")).strip()
                spanish = str(card.get("spanish", "")).strip()
                if prompt and spanish:
                    prompt_targets[(type_name, prompt)].append((spanish, loc))

                if prompt.startswith("听到 ") or "你要理解成什么" in prompt:
                    errors.append(
                        f"{loc}: listening-recognition prompt is stored as chunk_production."
                    )

                if " / " in spanish:
                    errors.append(
                        f"{loc}: chunk_production has multiple main answers in spanish={spanish}"
                    )

                if prompt.startswith("小段落：") and count_sentences(spanish) < 2:
                    errors.append(
                        f"{loc}: short paragraph prompt has only one Spanish sentence."
                    )
                if prompt.startswith("小段落：") and count_sentences(spanish) > 3:
                    errors.append(
                        f"{loc}: paragraph prompt has more than three Spanish sentences."
                    )

                for matcher, label in REUSABLE_CHUNK_PATTERNS:
                    if matcher.search(spanish) and not str(card.get("pattern", "")).strip():
                        errors.append(
                            f"{loc}: reusable chunk pattern is not labeled in pattern: {label}"
                        )

            elif type_name == "dialogue_response":
                question_es = str(card.get("question_es", "")).strip()
                answer_es = str(card.get("answer_es", "")).strip()

                if not question_es or not answer_es:
                    errors.append(
                        f"{loc}: dialogue_response must have both question_es and answer_es."
                    )
                if " / " in question_es or " / " in answer_es:
                    errors.append(f"{loc}: dialogue_response has multiple main Spanish answers.")

            elif type_name == "grammar_pattern":
                prompt = str(card.get("prompt_zh", "")).strip()
                answer_es = str(card.get("answer_es", "")).strip()
                if prompt and answer_es:
                    prompt_targets[(type_name, prompt)].append((answer_es, loc))
                if " / " in answer_es:
                    errors.append(f"{loc}: grammar_pattern answer tests multiple targets.")

            elif type_name == "mistake_contrast":
                correct_es = str(card.get("correct_es", "")).strip()
                wrong_es = str(card.get("wrong_es", "")).strip()
                explanation = str(card.get("explanation_zh", "")).strip()
                if " / " in correct_es:
                    errors.append(f"{loc}: mistake_contrast correct_es has multiple main answers.")
                if "___" in wrong_es:
                    errors.append(f"{loc}: mistake_contrast wrong_es is an incomplete choice.")
                if not explanation:
                    warnings.append(f"{loc}: mistake_contrast has no explanation_zh.")

            elif type_name == "vocabulary":
                prompt = str(card.get("prompt_zh", "")).strip()
                word_es = str(card.get("word_es", "")).strip()
                if prompt and word_es:
                    prompt_targets[(type_name, prompt)].append((word_es, loc))
                if any(mark in word_es for mark in ".?!。？！"):
                    warnings.append(f"{loc}: vocabulary word_es looks like a sentence: {word_es}")

    for (type_name, prompt), items in prompt_targets.items():
        targets = {target for target, _loc in items}
        if len(targets) > 1:
            refs = "; ".join(f"{loc} -> {target}" for target, loc in items)
            errors.append(
                f"{path.name}:{type_name}: same prompt_zh maps to multiple targets; "
                f"disambiguate the front prompt: {prompt!r}. {refs}"
            )

    return errors, warnings


def main() -> None:
    note_types = load_json(CONFIG_DIR / "note_types.json")
    errors: list[str] = []
    warnings: list[str] = []

    for path in sorted(CONTENT_DIR.glob("unidad_*.json")):
        file_errors, file_warnings = audit_file(path, note_types)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

    print("卡片设计审计")
    print("------------")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    print()

    if warnings:
        print("提醒")
        print("----")
        for warning in warnings[:MAX_WARNINGS_TO_PRINT]:
            print(f"- {warning}")
        if len(warnings) > MAX_WARNINGS_TO_PRINT:
            remaining = len(warnings) - MAX_WARNINGS_TO_PRINT
            print(f"- ... 还有 {remaining} 条提醒未显示。")
        print()

    if errors:
        print("审计失败")
        print("--------")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("审计通过。")


if __name__ == "__main__":
    main()
