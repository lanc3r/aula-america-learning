#!/bin/zsh
set -e
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "请先运行 build_deck.command。"
  read -k 1 "?按任意键关闭..."
  exit 1
fi

source venv/bin/activate
python scripts/build_deck.py --refresh_audio
open "release"
