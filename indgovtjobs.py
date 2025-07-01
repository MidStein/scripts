#!/usr/bin/env python

import json
import os
import sys
import requests
import subprocess

from datetime import date, timedelta
from typing import Any

from bs4 import BeautifulSoup, Tag


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
    anchorTag = tag.find("a")
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


def get_last_visited() -> tuple[dict[str, str], str]:
    with open(
        f"{os.path.dirname(__file__)}/last_visited_indgovtjobs.json"
    ) as last_visited_file:
        last_visited: Any = json.load(last_visited_file)
        return last_visited["posts"], last_visited["date"]


def update_last_visited(last_visited_posts: dict[str, str]) -> None:
    last_visited: dict[str, dict[str, str] | str] = {
        "posts": last_visited_posts,
        "date": str(date.today()),
    }
    with open(
        f"{os.path.dirname(__file__)}/last_visited_indgovtjobs.json", "w"
    ) as last_visited_file:
        json.dump(last_visited, last_visited_file, indent=2)


def prepare_email_body(new_jobs: dict[str, list[Job]]) -> str:
    body: str = ""
    for idx, category in enumerate(new_jobs.items()):
        if len(category[1]) != 0:
            body += "\n" if idx > 0 else ""
            body += f"## {category[0]}\n\n"
            for job in category[1]:
                body += f"- [{job.title}]({job.link})\n"
    return body


def main() -> None:
    last_visited_posts, last_visited_date = get_last_visited()

    if last_visited_date == str(date.today()) or last_visited_date == str(
        date.today() - timedelta(days=1)
    ):
        print("Email has already been sent")
        sys.exit()

    new_jobs: dict[str, list[Job]] = {}
    new_jobs_found: bool = False
    for url in URLS.items():
        tags: list[Tag] = fetch_job_elements(url[1])
        jobs: list[Job] = [parse_tag(tag) for tag in tags]
        new_jobs[url[0]] = extract_new_jobs(last_visited_posts[url[0]], jobs)

        if len(new_jobs[url[0]]) != 0:
            new_jobs_found = True
            last_visited_posts[url[0]] = new_jobs[url[0]][0].title

    if not new_jobs_found:
        print("No new jobs found from indgovtjobs.in")
        return
    update_last_visited(last_visited_posts)

    subject: str = "New jobs in www.indgovtjobs.in/2015/10/Government-Jobs.html"
    body: str = prepare_email_body(new_jobs)

    result: subprocess.CompletedProcess[str] = subprocess.run(
        [os.path.expanduser("~/scripts/gmail/self.py"), "-s", subject, "-b", body],
        capture_output=True,
        text=True,
    )
    print(result.stdout)


if __name__ == "__main__":
    main()
