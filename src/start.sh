#!/bin/zsh

cd "$(dirname "$0")" || exit 1

docker compose up -d >/dev/null
.venv/bin/python book_exam_app.py

