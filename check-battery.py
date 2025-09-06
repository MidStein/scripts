#!/usr/bin/env python

import subprocess


def main():
    with open("/sys/class/power_supply/BAT0/capacity") as sys_file:
        percentage: int = int(sys_file.readline().strip())

    if percentage == 100:
        subprocess.run(["notify-send", "Battery fully charged"])


if __name__ == "__main__":
    main()
