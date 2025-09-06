#!/usr/bin/env python

import os
import requests
import subprocess

from bs4 import BeautifulSoup, Tag


URL: str = "https://www.indgovtjobs.in/2014/04/it-fresher-jobs.html"


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


def get_last_visited() -> str:
    with open(
        f"{os.path.dirname(__file__)}/last_visited_indgovtjobs.txt"
    ) as last_visited_file:
        return last_visited_file.read().strip()


def update_last_visited(last_visited_post: str) -> None:
    with open(
        f"{os.path.dirname(__file__)}/last_visited_indgovtjobs.txt", "w"
    ) as last_visited_file:
        last_visited_file.write(last_visited_post)


def prepare_email_body(jobs: list[Job]) -> str:
    body: str = ""
    for job in jobs:
        body += f"- [{job.title}]({job.link})\n"
    return body


def main() -> None:
    last_visited = get_last_visited()

    new_jobs: list[Job] = []
    new_jobs_found: bool = False
    tags: list[Tag] = fetch_job_elements(URL)
    jobs: list[Job] = [parse_tag(tag) for tag in tags]
    new_jobs = extract_new_jobs(last_visited, jobs)

    if len(new_jobs) != 0:
        new_jobs_found = True
        last_visited = new_jobs[0].title

    if not new_jobs_found:
        print("No new jobs found from indgovtjobs.in")
        return
    update_last_visited(last_visited)

    subject: str = "New IT Engineer Jobs at www.indgovtjobs.in"
    body: str = prepare_email_body(new_jobs)

    result: subprocess.CompletedProcess[str] = subprocess.run(
        [os.path.expanduser("~/scripts/gmail/self.py"), "-s", subject, "-b", body],
        capture_output=True,
        text=True,
    )
    print(result.stdout)


if __name__ == "__main__":
    main()
