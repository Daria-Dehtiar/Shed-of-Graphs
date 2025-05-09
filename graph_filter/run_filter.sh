#!/bin/bash

if [ "$#" -lt 2 ]; then
  echo "Usage: ../run_filter.sh <number_of_vertices> <rules_json> [--export image_folder] [--image_format format]" >&2
  exit 1
fi

VERTICES=$1
FILTER="$2"

if ! [[ "$VERTICES" =~ ^[0-9]+$ ]]; then
  echo "Error: number_of_vertices must be a positive integer." >&2
  exit 1
fi

shift 2

HISTORY_DIR="${HOME}/.history"
mkdir -p "$HISTORY_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
HISTORY_FILE="${HISTORY_DIR}/history_${VERTICES}_${TIMESTAMP}.log"

nauty-geng "$VERTICES" | python3 "$(dirname "$0")/filter_main.py" "$FILTER" "$HISTORY_FILE" "$@"