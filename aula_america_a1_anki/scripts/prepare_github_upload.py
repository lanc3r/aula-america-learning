from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "github_upload"

EXCLUDED_DIRS = {
    "audio_cache",
    "output",
    "github_upload",
    "venv",
    "__pycache__"
}

def should_copy(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    return not any(part in EXCLUDED_DIRS for part in relative.parts)

def main() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir()

    for path in ROOT.rglob("*"):
        if not should_copy(path):
            continue
        relative = path.relative_to(ROOT)
        destination = TARGET / relative

        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)

    print(f"GitHub 上传目录已生成：{TARGET}")
    print("该目录不包含 audio_cache、output、venv 或 API key。")

if __name__ == "__main__":
    main()
