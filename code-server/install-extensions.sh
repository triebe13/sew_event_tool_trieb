#!/usr/bin/env bash
set -e

CODESERVER="/app/code-server/bin/code-server"
EXT_DIR="/config/extensions"

mkdir -p $EXT_DIR

# $CODESERVER --extensions-dir $EXT_DIR --install-extension ms-python.vscode-pylance
$CODESERVER --extensions-dir $EXT_DIR --install-extension ms-python.python
$CODESERVER --extensions-dir $EXT_DIR --install-extension ms-pyright.pyright
$CODESERVER --extensions-dir $EXT_DIR --install-extension ms-python.isort
$CODESERVER --extensions-dir $EXT_DIR --install-extension formulahendry.code-runner
$CODESERVER --extensions-dir $EXT_DIR --install-extension ecmel.vscode-html-css
$CODESERVER --extensions-dir $EXT_DIR --install-extension bradlc.vscode-tailwindcss
$CODESERVER --extensions-dir $EXT_DIR --install-extension tamasfe.even-better-toml
$CODESERVER --extensions-dir $EXT_DIR --install-extension akamud.vscode-theme-onedark

$CODESERVER --extensions-dir $EXT_DIR --install-extension jebbs.plantuml
# Markdown Preview Enhanced (for advanced markdown rendering)
$CODESERVER --extensions-dir $EXT_DIR --install-extension shd101wyy.markdown-preview-enhanced
