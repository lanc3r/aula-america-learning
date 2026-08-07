from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
CONTENT_DIR = ROOT / "content"

FILENAME_PATTERN = re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9]+)?$")

IGNORED_DIRECTORIES = {
    "venv",
    "__pycache__",
    "audio_cache",
    "output",
    "release",
    "github_upload",
    ".git",
}

QUESTION_FIELDS = {"spanish", "question_es", "target_es", "contrast_es"}

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_filenames() -> list[str]:
    errors: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(ROOT)

        # Only validate maintained project source files.
        # Generated environments, caches, releases, and hidden metadata
        # are intentionally excluded.
        if any(part in IGNORED_DIRECTORIES for part in relative.parts):
            continue

        if any(part.startswith(".") for part in relative.parts):
            continue

        if not FILENAME_PATTERN.match(path.name):
            errors.append(f"非法文件名：{relative}")

    return errors

def validate_contract(
    deck_config: dict[str, Any],
    note_types: dict[str, Any]
) -> list[str]:
    payload = {
        key: {
            "model_id": value["model_id"],
            "model_name": value["model_name"],
            "fields": value["fields"],
            "template_name": value["template_name"]
        }
        for key, value in note_types["note_types"].items()
    }
    current_hash = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    if current_hash != deck_config["contract_hash"]:
        return [
            "Note Type 契约发生变化。除非明确执行不兼容升级，"
            "否则不要修改 model_id、字段顺序、模板数量或模板名称。"
        ]
    return []

def validate_content(
    note_types: dict[str, Any],
    retired_uids: set[str]
) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    seen_uids: set[str] = set()
    counts = {key: 0 for key in note_types["note_types"]}

    content_files = sorted(CONTENT_DIR.glob("unidad_*.json"))
    if not content_files:
        return ["没有找到 content/unidad_*.json。"], counts

    for path in content_files:
        data = load_json(path)
        cards = data.get("cards", {})

        unknown_types = set(cards) - set(note_types["note_types"])
        for unknown in sorted(unknown_types):
            errors.append(f"{path.name} 包含未知卡片类型：{unknown}")

        for type_name, spec in note_types["note_types"].items():
            entries = cards.get(type_name, [])
            if not isinstance(entries, list):
                errors.append(f"{path.name}: {type_name} 必须是列表。")
                continue

            counts[type_name] += len(entries)
            required = set(spec["required_content_fields"])

            for index, card in enumerate(entries, start=1):
                location = f"{path.name}:{type_name}[{index}]"
                missing = required - set(card)
                if missing:
                    errors.append(
                        f"{location} 缺少字段：{', '.join(sorted(missing))}"
                    )

                uid = str(card.get("uid", "")).strip()
                if not uid:
                    errors.append(f"{location} 缺少 uid。")
                elif uid in seen_uids:
                    errors.append(f"{location} UID 重复：{uid}")
                elif uid in retired_uids:
                    errors.append(f"{location} 复用了 retired UID：{uid}")
                else:
                    seen_uids.add(uid)

                tags = card.get("tags")
                if tags is not None and (
                    not isinstance(tags, list)
                    or not all(isinstance(tag, str) and tag for tag in tags)
                ):
                    errors.append(f"{location} tags 必须是非空字符串列表。")

                for field in spec["audio_content_fields"]:
                    value = str(card.get(field, "")).strip()
                    if not value:
                        continue
                    if value.endswith("?") and not value.startswith("¿"):
                        errors.append(
                            f"{location} 西语问句缺少倒问号：{field}={value}"
                        )
                    if value.endswith("!") and not value.startswith("¡"):
                        errors.append(
                            f"{location} 西语感叹句缺少倒感叹号：{field}={value}"
                        )

    return errors, counts

def main() -> None:
    deck_config = load_json(CONFIG_DIR / "deck_config.json")
    note_types = load_json(CONFIG_DIR / "note_types.json")
    retired_data = load_json(CONTENT_DIR / "retired_uids.json")
    retired_uids = set(retired_data.get("retired_uids", []))

    errors: list[str] = []
    errors.extend(validate_filenames())
    errors.extend(validate_contract(deck_config, note_types))
    content_errors, counts = validate_content(note_types, retired_uids)
    errors.extend(content_errors)

    print("内容统计")
    print("--------")
    total = 0
    for type_name, count in counts.items():
        print(f"{type_name}: {count}")
        total += count
    print(f"total: {total}")
    print()

    if errors:
        print("验证失败")
        print("--------")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("验证通过。")

if __name__ == "__main__":
    main()
