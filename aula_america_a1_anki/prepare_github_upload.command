#!/bin/zsh
set -e
cd "$(dirname "$0")"
python3 scripts/prepare_github_upload.py
open "github_upload"
