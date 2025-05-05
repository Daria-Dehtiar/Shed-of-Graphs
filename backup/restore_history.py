import os
import sys
import shutil

BACKUP_DIR = os.path.expanduser("~/.filtered-graphs")
HISTORY_DIR = os.path.expanduser("~/.history")


def list_backups():
    contents = os.listdir(BACKUP_DIR)
    backups = []

    for item in contents:
        if item.endswith(".log"):
            backups.append(item)

    f = lambda x: os.path.getctime(os.path.join(BACKUP_DIR, x))
    backups.sort(key=f)
    return backups


def select_backup(backups):
    print("Available backups:")

    for i, backup in enumerate(backups):
        print(f"[{i+1}] {backup}")

    choice = input("Enter the number of the backup you would like to restore: ")

    try:
        index = int(choice) - 1
        return backups[index]
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number.", file = sys.stderr)
        sys.exit(1)


def restore_backup(backup_filename):
    dst_file = backup_filename.split("__backup_of_")[1]
    dst_file_path = os.path.join(HISTORY_DIR, dst_file)
    src_file_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        shutil.copy2(src_file_path, dst_file_path)
        print(f"Content successfully restored from {backup_filename} to {dst_file_path}.")
    except Exception as e:
        print(f"Failed to restore: {e}", file=sys.stderr)
        sys.exit(1)



def main():
    for path in (BACKUP_DIR, HISTORY_DIR):
        if not os.path.exists(path):
            print(f"Required directory is missing: {path}", file=sys.stderr)
            exit(1)

    backups = list_backups()
    if not backups:
        print("No backups found.")
        return

    selected_backup = select_backup(backups)

    confirm = input(f"Do you want to restore {selected_backup}? This will overwrite the original history file. [Y/n]: ")
    if confirm.lower() != "y":
        print("Restore cancelled.")
        return

    restore_backup(selected_backup)


if __name__ == "__main__":
    main()