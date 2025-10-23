#!/bin/bash
cd /config/workspace/backend/
uv venv ./.venv --clear
source ./.venv/bin/activate
uv sync --active


