#!/bin/zsh
set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "没有找到 python3。请先安装 Python 3.9 或更新版本。"
  read -k 1 "?按任意键关闭..."
  exit 1
fi

if [ ! -d "venv" ]; then
  echo "第一次运行：创建独立 Python 环境……"
  python3 -m venv venv
fi

source venv/bin/activate
python -m pip install --disable-pip-version-check --quiet --upgrade pip
python -m pip install --disable-pip-version-check --quiet -r requirements.txt

python scripts/build_deck.py
open "release"
