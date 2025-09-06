from datetime import datetime, timedelta, timezone
import os.path

import google.auth.external_account_authorized_user

from pathlib import Path
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from scopes import SCOPES


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


def main():
    creds: Credentials = get_credentials()
    service: Any = build("calendar", "v3", credentials=creds)

    today: datetime = datetime.now(timezone.utc)
    two_weeks_ago: datetime = today - timedelta(weeks=2)
    time_min: str = two_weeks_ago.isoformat().replace("+00:00", "Z")
    time_max: str = today.isoformat().replace("+00:00", "Z")
    response: dict = (
        service.events()
        .list(
            calendarId="primary",
            singleEvents=True,
            timeMin=time_min,
            timeMax=time_max,
        )
        .execute()
    )

    cnt: int = 0
    for event in response.get("items", []):
        start = event.get("start", {}).get("dateTime") or event.get("start", {}).get(
            "date"
        )
        end = event.get("end", {}).get("dateTime") or event.get("end", {}).get("date")

        if start == end:
            service.events().delete(calendarId="primary", eventId=event["id"]).execute()
            cnt += 1

    print(f"{cnt} reminders deleted")


if __name__ == "__main__":
    main()
