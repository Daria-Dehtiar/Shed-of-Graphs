#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/backup_history.py"
PYTHON_BIN=$(which python3)
LOG_FILE=~/.backup_history.log

if [ ! -f "$SCRIPT_PATH" ]; then
  echo "Error: Could not find backup_history.py at $SCRIPT_DIR" >&2
  exit 1
fi

if crontab -l 2>/dev/null | grep -Fq "$SCRIPT_PATH"; then
  echo "Cron job already exists."
else
  (crontab -l 2>/dev/null; echo "0 * * * * $PYTHON_BIN $SCRIPT_PATH >> $LOG_FILE 2>&1") | crontab -
  echo "Cron job added to run backups hourly."
fi