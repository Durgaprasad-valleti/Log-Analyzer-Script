
import csv

def save_logs_csv(logs, path):
    if not logs:
        print("No logs to save.")
        return
    fieldnames = list(logs[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for log in logs:
            writer.writerow(log)
