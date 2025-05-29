import argparse
import random
import sys

parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("-c", type=int, help="count of random outputs")
args: argparse.Namespace = parser.parse_args()

lines: list[str] = sys.stdin.read().splitlines()
count: int
if args.c:
    count = args.c
elif len(lines) < 5:
    count = len(lines)
else:
    count = 5
if count > len(lines):
    raise Exception(f"Range too small for generating {count} random numbers")

lines = [line.strip() for line in lines]
for line in random.sample(lines, count):
    print(line)
