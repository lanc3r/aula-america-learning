#!/bin/zsh
set -e
cd "$(dirname "$0")"
python3 scripts/validate_content.py
python3 scripts/audit_card_design.py
echo
read -k 1 "?按任意键关闭..."
