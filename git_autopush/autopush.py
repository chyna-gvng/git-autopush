import os
import time
import subprocess
import signal
import sys

def monitor_directory(path="."):
    if not os.path.exists(os.path.join(path, ".git")):
        print("Directory is not a Git repo!")
        return

    print("Monitoring...")

    files = {}

    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            files[full_path] = os.stat(full_path).st_mtime

    def exit_gracefully(signal, frame):
        print("\nGoodbye!")
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_gracefully)

    try:
        while True:
            current_files = {filename: os.stat(filename).st_mtime for filename in files.keys()}

            added_files = current_files.keys() - files.keys()
            deleted_files = files.keys() - current_files.keys()
            modified_files = {
                filename for filename in files.keys() & current_files.keys()
                if files[filename] != current_files[filename]
            }

            changes_detected = False  # Flag to track if changes were detected

            for file in added_files:
                commit_message = f"Created {os.path.basename(file)}"
                add_and_push(file, commit_message)
                changes_detected = True

            for file in deleted_files:
                commit_message = f"Deleted {os.path.basename(file)}"
                add_and_push(file, commit_message)
                changes_detected = True

            for file in modified_files:
                commit_message = f"Updated {os.path.basename(file)}"
                add_and_push(file, commit_message)
                changes_detected = True

            files = current_files

            if not changes_detected:
                time.sleep(1)  # Sleep for 1 second before checking again

    except KeyboardInterrupt:
        exit_gracefully(None, None)

def add_and_push(file, commit_message):
    subprocess.run(["git", "add", file])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    monitor_directory()
