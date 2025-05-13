import csv
import datetime
import os

def log_event(username, role, action):
    log_file = "usage_log.csv"
    file_exists = os.path.exists(log_file)

    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Username", "Role", "Action"])
        writer.writerow([
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            username,
            role,
            action
        ])
