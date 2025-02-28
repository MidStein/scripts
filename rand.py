import argparse
import secrets
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
    print(f"Range too small for generating {count} random numbers")
    exit()

numbers: list[int] = []
while len(numbers) < count:
    rand: int = secrets.randbelow(len(lines)) + 1
    if rand not in numbers:
        print(lines[rand - 1].strip())
        numbers.append(rand)
