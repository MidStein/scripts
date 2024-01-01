#!/usr/bin/env python3

import secrets
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--min", type=int)
parser.add_argument("--max", type=int)
parser.add_argument("-c", type=int,
                    help="count of random numbers")
args = parser.parse_args()

min = args.min if args.min else 1
count = args.c if args.c else 1

for _ in range(count):
    print(secrets.randbelow(args.max - min + 1) + min, end=' ')

print()

