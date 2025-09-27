import csv
import os
from datetime import datetime

LOG_FILE = "activity_log.csv"

# Ensure CSV has headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "user_input", "ai_reply", "flagged", "pii_detected", "blocked"])

def log_activity(user_input, ai_reply, flagged, pii_detected, blocked=False):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_input,
            ai_reply,
            flagged,
            pii_detected,
            blocked
        ])

def reset_logs():
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "user_input", "ai_reply", "flagged", "pii_detected", "blocked"])
