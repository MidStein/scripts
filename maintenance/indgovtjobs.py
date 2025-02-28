#!/usr/bin/env python

import argparse
import json
import os
import requests
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup, NavigableString, Tag


EMAIL_SENDER_ADDRESS: str = "deepakchauhan19feb@gmail.com"
EMAIL_RECEIVER_ADDRESS: str = "deepakchauhan19feb@gmail.com"
EMAIL_SUBJECT: str = "New jobs in www.indgovtjobs.in/2015/10/Government-Jobs.html"
URLS: dict[str, str] = {
    "B.Tech Engineer Govt Jobs": "https://www.indgovtjobs.in/2013/09/government-jobs-for-engineers-2013-2014.html",
    "Degree Graduate Govt Jobs": "https://www.indgovtjobs.in/2013/09/government-jobs-for-graduates-2013-2014.html",
    "IT Engineer Jobs": "https://www.indgovtjobs.in/2014/04/it-fresher-jobs.html",
}


class Job:
    def __init__(self, title: str, company: str, link: str):
        self.title = title
        self.company = company
        self.link = link

    def __str__(self) -> str:
        return self.title


def fetch_job_elements(url: str) -> list[Tag]:
    response: requests.Response = requests.get(url)

    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    table = soup.select(".post-body.entry-content")[0].select(
        "table:first-of-type>tbody"
    )[0]
    return table.select("tr")[1:]


def parse_tag(tag: Tag) -> Job:
    title: str = tag.contents[1].get_text().strip()
    company: str = tag.contents[5].get_text().strip()
    anchorTag: Tag | NavigableString | None = tag.find("a")
    if not isinstance(anchorTag, Tag):
        raise Exception("unexpected!")
    link: str | list[str] | None = anchorTag.get("href")
    if not isinstance(link, str):
        raise Exception("unexpected!")
    return Job(title=title, company=company, link=link)


def extract_new_jobs(last_visited_job: str, fetched_jobs: list[Job]) -> list[Job]:
    new_jobs: list[Job] = []
    for job in fetched_jobs:
        if job.title == last_visited_job:
            break
        new_jobs.append(job)
    return new_jobs


def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-p", required=True, type=ascii, help="app password")
    return parser.parse_args()


def get_last_visited_jobs() -> dict[str, str]:
    with open(f"{os.path.dirname(__file__)}/last_visited_indgovtjobs.json") as last_visited_file:
        return json.load(last_visited_file)


def update_last_visited_jobs(last_visited_jobs: dict[str, str]) -> None:
    with open(f"{os.path.dirname(__file__)}/last_visited_indgovtjobs.json", "w") as last_visited_file:
        json.dump(last_visited_jobs, last_visited_file, indent=2)


def prepare_email_body(new_jobs: dict[str, list[Job]]) -> str:
    body: str = ""
    for category in new_jobs.items():
        if len(category[1]) != 0:
            body += f"<h2>{category[0]}</h2>"
            body += "<ul>"
            for job in category[1]:
                body += f"<li><a href={job.link}>{job.title} in {job.company}</a></li>"
            body += "</ul>"
    return body


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
    last_visited_jobs: dict[str, str] = get_last_visited_jobs()

    args: argparse.Namespace = parse_arguments()

    new_jobs: dict[str, list[Job]] = {}
    new_jobs_found: bool = False
    for url in URLS.items():
        tags: list[Tag] = fetch_job_elements(url[1])
        jobs: list[Job] = [parse_tag(tag) for tag in tags]
        new_jobs[url[0]] = extract_new_jobs(last_visited_jobs[url[0]], jobs)

        if len(new_jobs[url[0]]) != 0:
            new_jobs_found = True
            last_visited_jobs[url[0]] = new_jobs[url[0]][0].title

    if not new_jobs_found:
        print("No new jobs found from indgovtjobs.in")
        return
    update_last_visited_jobs(last_visited_jobs)

    body: str = prepare_email_body(new_jobs)

    smtp_password: str = args.p.strip("'")

    send_email(
        EMAIL_SENDER_ADDRESS, EMAIL_RECEIVER_ADDRESS, EMAIL_SUBJECT, body, smtp_password
    )
    print("New email sent by indgovtjobs")


if __name__ == "__main__":
    main()
