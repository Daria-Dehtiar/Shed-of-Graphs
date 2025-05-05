#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: ../run_filter_in_parallel.sh <number_of_vertices> <rules_json> <number_of_batches>" >&2
  exit 1
fi

VERTICES=$1
FILTER="$2"
BATCHES=$3

if ! [[ "$VERTICES" =~ ^[0-9]+$ ]] || ! [[ "$BATCHES" =~ ^[0-9]+$ ]]; then
  echo "Error: number_of_vertices and number_of_batches must be positive integers." >&2
  exit 1
fi

HISTORY_PAR_DIR="${HOME}/.history_parallel"
mkdir -p "$HISTORY_PAR_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)


for RES in $(seq 0 $((BATCHES -1))); do
  (
  echo "Starting batch $RES/$BATCHES"

  HISTORY_PAR_FILE="${HISTORY_PAR_DIR}/history_batch_${RES}_of_${BATCHES}_${VERTICES}_${TIMESTAMP}.log"
  nauty-geng "$VERTICES" -q ${RES}/${BATCHES}  | python3 ../graph_filter.py "$FILTER" "$HISTORY_PAR_FILE" > /dev/null

  echo "Finished batch $RES/$BATCHES"
  ) &
done

wait
echo "All batches completed."


python3 merge_history.py "$TIMESTAMP" "$VERTICES" "$FILTER"