import threading
import os
import time
from Jarvis import main

log_file = os.path.join(os.getcwd(), "templates", "log.txt")


def display_log():
    """Continuously dis/ for carryminatiplay the log file's content in real time."""
    last_position = 0  # Keep track of last read position

    while True:
        try:
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    f.seek(last_position)  # Move to last read position
                    new_logs = f.read()  # Read new content

                    if new_logs:
                        print(new_logs.strip())  # Print new logs
                        last_position = f.tell()  # Update position

            else:
                print("[LOG] No log file found. Waiting for entries...")

        except Exception as e:
            print(f"[ERROR] Log monitoring error: {e}")

        time.sleep(2)  # Sleep for 2 seconds before checking again


def run_terminal():
    """Start Jarvis and log monitoring in parallel."""
    t1 = threading.Thread(target=main, daemon=True)
    t2 = threading.Thread(target=display_log, daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    run_terminal()
