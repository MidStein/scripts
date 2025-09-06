#!/usr/bin/env python

import os.path
import socket
import subprocess
import sys

import psutil

from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from scopes import SCOPES


def is_connected_to_wifi() -> bool:
    for _, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address == "127.0.0.1":
                return True
    return False


def get_credentials() -> Credentials:
    tokenFilePath: Path = Path(os.path.dirname(__file__), "token.json")

    creds = None
    if os.path.exists(tokenFilePath):
        creds = Credentials.from_authorized_user_file(tokenFilePath, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            Path(os.path.dirname(__file__), "credentials.json"), SCOPES
        )
        creds = flow.run_local_server(port=0, access_type="offline")
        with open(tokenFilePath, "w") as token:
            token.write(creds.to_json())

    if isinstance(creds, Credentials):
        return creds
    else:
        raise Exception(
            "isinstance(creds, google.auth.external_account_authorized_user) should not be true"
        )


def main():
    if not is_connected_to_wifi():
        print("Not connected to Wi-Fi. Exiting.")
        sys.exit(1)

    creds: Credentials = get_credentials()
    service: Any = build("gmail", "v1", credentials=creds)
    results: dict = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX", "UNREAD"])
        .execute()
    )

    if results.get("resultSizeEstimate") == 0:
        print("0 unread emails.")
        sys.exit()

    messages: list[dict[str, str]] = results.get("messages", [])
    subprocess.run(
        ["notify-send", "gmail-notifier", f"You have {len(messages)} unread email(s)."],
    )


if __name__ == "__main__":
    main()
