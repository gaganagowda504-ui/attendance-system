import csv
from datetime import datetime
def mark_attendance(name):
    with open("attendance.csv", "r+") as f:
        data = f.readlines()
        names = []

        for line in data:
            entry = line.split(",")
            names.append(entry[0])

        if name not in names:
            now = datetime.now()
            dt = now.strftime("%Y-%m-%d,%H:%M:%S")

            f.writelines(f"\n{name},{dt}")