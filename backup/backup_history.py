import os
import sys
from datetime import datetime
import shutil


HISTORY_DIR = os.path.expanduser("~/.history")
BACKUP_DIR = os.path.expanduser("~/.filtered-graphs")


def create_backup(history_file_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)

    history_filename = os.path.basename(history_file_path)
    history_filename_wout_ext = os.path.splitext(history_filename)[0]
    timestamp = datetime.now().strftime("%H-%M-%S")

    backup_history_filename = f"({timestamp})__backup_of_{history_filename_wout_ext}.log"
    backup_history_file_path = os.path.join(BACKUP_DIR, backup_history_filename)

    try:
        shutil.copy2(history_file_path, backup_history_file_path)
        print(f"[{timestamp}] Backup created for {history_filename} at {backup_history_file_path}")
    except Exception as e:
        print(f"[{timestamp}] Failed to back up {history_filename}: {e}", file=sys.stderr)


def create_backup_for_all():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print("\n" + f"========== [{timestamp}] Starting backup process...")
    if not os.path.exists(HISTORY_DIR):
        print(f"The history directory {HISTORY_DIR} does not exist.", file=sys.stderr)
        return

    for filename in os.listdir(HISTORY_DIR):
        full_path = os.path.join(HISTORY_DIR, filename)

        if os.path.isfile(full_path) and filename.endswith(".log"):
            create_backup(full_path)
    print(f"========== Backup process completed.")



if __name__ == "__main__":
    create_backup_for_all()