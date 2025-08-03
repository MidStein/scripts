#!/usr/bin/env python

import argparse
import base64
import os.path
import socket
import sys

import google.auth.external_account_authorized_user
import psutil

from dataclasses import dataclass
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from scopes import SCOPES


def is_connected_to_wifi() -> bool:
    for _, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address == "127.0.0.1":
                return True
    return False


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-s", help="Email subject", required=True)
    parser.add_argument("-b", help="Email body")
    parser.add_argument("-t", help="Unix timestamp")
    return parser.parse_args()


@dataclass
class Event:
    summary: str
    description: str
    dateTime: str

    def to_dict(self) -> dict:
        return {
            "summary": self.summary,
            "description": self.description,
            "start": {
                "dateTime": self.dateTime,
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": self.dateTime,
                "timeZone": "UTC",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [{"method": "email", "minutes": 0}],
            },
        }


def get_credentials() -> Credentials:
    tokenFilePath: Path = Path(os.path.dirname(__file__), "token.json")
    if os.path.exists(tokenFilePath):
        creds: Credentials = Credentials.from_authorized_user_file(
            tokenFilePath, SCOPES
        )
        if not creds or not creds.valid:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                Path(os.path.dirname(__file__), "credentials.json"), SCOPES
            )
            new_creds: (
                Credentials | google.auth.external_account_authorized_user.Credentials
            ) = flow.run_local_server(port=0)
            if isinstance(new_creds, Credentials):
                creds = new_creds
            else:
                raise Exception(
                    "isinstance(creds, google.auth.external_account_authorized_user) should not be true"
                )
            with open(tokenFilePath, "w") as token:
                token.write(creds.to_json())
        return creds
    raise Exception


def create_message(subject, message_text):
    message: MIMEText = MIMEText(message_text)
    message["to"] = "deepakchauhan19feb@gmail.com"
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}


def main():
    args: argparse.Namespace = parse_args()

    if not is_connected_to_wifi():
        print("Not connected to Wi-Fi. Exiting.")
        sys.exit(1)

    creds: Credentials = get_credentials()

    if args.t:
        service: Any = build("calendar", "v3", credentials=creds)

        time: str = datetime.fromtimestamp(int(args.t), tz=timezone.utc).isoformat()
        event: Event = Event(
            summary=args.s, description="" if not args.b else args.b, dateTime=time
        )

        event_result: dict = (
            service.events()
            .insert(calendarId="primary", body=event.to_dict())
            .execute()
        )
        print(f"Event created: {event_result.get('htmlLink')}")
    else:
        service: Any = build("gmail", "v1", credentials=creds)

        message: dict[str, str] = create_message(args.s, "" if not args.b else args.b)

        service.users().messages().send(userId="me", body=message).execute()
        print("Email sent succesfully!")


if __name__ == "__main__":
    main()
