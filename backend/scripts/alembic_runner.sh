#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <alembic command and parameters>"
    echo "Example: $0 upgrade head"
    echo "         $0 revision --autogenerate -m \"init migration\""
    exit 1
fi


# Escape double quotes and build command string
escaped_args=()
for arg in "$@"; do
    escaped_arg="${arg//\"/\\\"}"
    escaped_args+=("$escaped_arg")
done

command_str="alembic ${escaped_args[*]}"

echo "Executing command: $command_str"

json_payload=$(printf '{"cmd": "%s"}' "$command_str")

curl -X 'POST' \
  'http://backend:8000/api/execute_command/run' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "$json_payload"