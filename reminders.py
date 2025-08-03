#!/usr/bin/env python

import json
import os.path
import subprocess
import sys

from datetime import datetime, time
from pathlib import Path

from pydantic import BaseModel


class Reminder(BaseModel):
    name: str
    time: str
    days: str


def main():
    with open(Path(os.path.dirname(__file__), "reminders.json")) as reminders_json:
        raw_reminders: list[dict[str, str]] = json.load(reminders_json)
    reminders: list[Reminder] = [Reminder(**reminder) for reminder in raw_reminders]

    today: datetime = datetime.now()
    for reminder in reminders:
        if str(today.weekday() + 1) in reminder.days:
            timePart: time = datetime.strptime(reminder.time, "%I:%M%p").time()
            result: subprocess.CompletedProcess[bytes] = subprocess.run(
                [
                    os.path.expanduser("~/scripts/gmail/self.py"),
                    "-s",
                    reminder.name,
                    "-t",
                    str(int(datetime.combine(today.date(), timePart).timestamp())),
                ]
            )
            if result.returncode == 1:
                sys.exit(1)
            print(f"Reminder created. name={reminder.name}, time={reminder.time}")


if __name__ == "__main__":
    main()
