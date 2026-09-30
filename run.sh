#!/bin/bash
cd "$(dirname "$0")"

[ -d "venv" ] || python3 -m venv venv
. venv/bin/activate

python main.py
