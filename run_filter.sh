#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: ./run_filter.sh <number_of_vertices> <rules_json>" >&2
  exit 1
fi

NODES=$1
FILTER="$2"

if ! [[ "$NODES" =~ ^[0-9]+$ ]]; then
  echo "Error: number_of_vertices must be a positive integer." >&2
  exit 1
fi

geng "$NODES" | python3 graph_filter.py "$FILTER"