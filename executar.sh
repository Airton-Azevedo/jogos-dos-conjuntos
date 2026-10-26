#!/usr/bin/env bash
# Inicia o jogo a partir da pasta do projeto.
cd "$(dirname "$0")" || exit 1

if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

python3 main.py
