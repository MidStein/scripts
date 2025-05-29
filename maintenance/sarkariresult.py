#!/usr/bin/env python

import argparse
import json
import requests
import os
import smtplib
import sys

from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from bs4 import BeautifulSoup, Tag


EMAIL_SENDER_ADDRESS = "deepakchauhan19feb@gmail.com"
EMAIL_RECEIVER_ADDRESS = "deepakchauhan19feb@gmail.com"
EMAIL_SUBJECT = "New jobs in www.sarkariresult.com/latestjob/"


class Job:
    def __init__(self, post: str, link: str):
        self.post = post
        self.link = link

    def __str__(self) -> str:
        return self.post


def fetch_job_elements() -> list[Tag]:
    url: str = "http://www.sarkariresult.com/latestjob/"
    css_selector: str = "#post>ul"

    response: requests.Response = requests.get(url)

    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    return soup.select(css_selector)


def parse_tag(tag: Tag) -> Job:
    anchorTag = tag.find("a")
    if not isinstance(anchorTag, Tag):
        raise Exception("unexpected!")
    post: str = anchorTag.get_text(strip=True)
    link = anchorTag.get("href")
    if not isinstance(link, str):
        raise Exception("unexpected!")
    return Job(post=post, link=link)


def extract_new_jobs(last_visited_post: str, fetched_jobs: list[Job]) -> list[Job]:
    new_jobs: list[Job] = []
    for job in fetched_jobs:
        if job.post == last_visited_post:
            break
        new_jobs.append(job)
    return new_jobs


def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-p", required=True, type=ascii, help="app password")
    return parser.parse_args()


def get_last_visited() -> tuple[str, str]:
    with open(
        f"{os.path.dirname(__file__)}/last_visited_sarkariresult.json"
    ) as last_visited_file:
        last_visited: Any = json.load(last_visited_file)
        return last_visited["post"], last_visited["date"]


def update_last_visited(last_visited_post: str) -> None:
    last_visited: dict[str, str] = {
        "post": last_visited_post,
        "date": str(date.today())
    }
    with open(
        f"{os.path.dirname(__file__)}/last_visited_sarkariresult.json", "w"
    ) as last_visited_file:
        json.dump(last_visited, last_visited_file, indent=2)


def prepare_email_body(new_jobs: list[Job]) -> str:
    list_items: list[str] = [
        f"<li><a href={job.link}>{job.post}</a></li>" for job in new_jobs
    ]
    return f"<ul>{"".join(list_items)}</ul>"


def send_email(
    sender_address: str,
    receiver_address: str,
    subject: str,
    body: str,
    smtp_password: str,
) -> None:
    msg: MIMEMultipart = MIMEMultipart()
    msg["From"] = sender_address
    msg["To"] = receiver_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_address, smtp_password)
        server.sendmail(sender_address, receiver_address, msg.as_string())


def main() -> None:
    last_visited_post, last_visited_date = get_last_visited()

    if (
        last_visited_date == str(date.today())
        or last_visited_date == str(date.today() - timedelta(days=1))
    ):
        print("Email has already been sent")
        sys.exit()

    args: argparse.Namespace = parse_arguments()

    tags: list[Tag] = fetch_job_elements()
    jobs: list[Job] = [parse_tag(tag) for tag in tags]
    new_jobs: list[Job] = extract_new_jobs(last_visited_post, jobs)

    if not new_jobs:
        print("No new jobs found from sarkariresult.com")
        return
    update_last_visited(new_jobs[0].post)

    body: str = prepare_email_body(new_jobs)

    smtp_password: str = args.p.strip("'")

    send_email(
        EMAIL_SENDER_ADDRESS, EMAIL_RECEIVER_ADDRESS, EMAIL_SUBJECT, body, smtp_password
    )
    print("New email sent by sarkariresult")


if __name__ == "__main__":
    main()
