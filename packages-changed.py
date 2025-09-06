#!/usr/bin/env python

import difflib
import re
import subprocess
import os

from itertools import count
from subprocess import CompletedProcess
from typing import Iterator


def get_previous_packages() -> list[str]:
    with open(os.path.expanduser("~/keep/packages.md")) as packages_md:
        file_lines: list[str] = packages_md.readlines()
    package_lines: list[str] = []
    for line_number in count(3):
        if file_lines[line_number - 1].strip() == "":
            package_lines = file_lines[2 : line_number - 1]
            break
    package_lines = [line.strip() for line in package_lines]
    package_lines = [line[2:] for line in package_lines]
    package_lines = [re.sub(r" .*", "", line) for line in package_lines]
    return package_lines


def get_explicit_packages() -> list[str]:
    result: CompletedProcess[bytes] = subprocess.run(
        ["pacman", "-Qe"], capture_output=True
    )
    packages: list[str] = result.stdout.decode().strip().split("\n")
    packages = [re.sub(r" .*", "", package) for package in packages]
    return packages


def remove_required_packages(packages: list[str]) -> list[str]:
    result_packages: list[str] = []
    for package in packages:
        process_result: CompletedProcess[bytes] = subprocess.run(
            ["pacman", "-Qi", package], capture_output=True
        )
        result_lines: list[str] = process_result.stdout.decode().strip().split("\n")
        for line in result_lines:
            if "Required By" in line:
                if "None" in line:
                    result_packages.append(package)
                break
    return result_packages


def get_current_packages() -> list[str]:
    explicit_packages: list[str] = get_explicit_packages()
    explicit_packages = remove_required_packages(explicit_packages)
    return explicit_packages


def main() -> None:
    previous_packages: list[str] = get_previous_packages()
    current_packages: list[str] = get_current_packages()
    differ: difflib.Differ = difflib.Differ()
    diff: Iterator[str] = differ.compare(previous_packages, current_packages)
    filtered_diff: list[str] = [line for line in diff if not line.startswith(" ")]
    if filtered_diff:
        print("\n".join(filtered_diff))
    else:
        print("No packages changed.")


if __name__ == "__main__":
    main()
