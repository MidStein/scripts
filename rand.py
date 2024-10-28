import argparse
import secrets
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-c", type=int, help="count of random outputs")
args = parser.parse_args()

lines = sys.stdin.read().splitlines()
if args.c:
    count = args.c
elif len(lines) < 5:
    count = len(lines)
else:
    count = 5
if count > len(lines):
    print(f"Range too small for generating {count} random numbers")
    exit()

numbers = []
while len(numbers) < count:
    rand = secrets.randbelow(len(lines)) + 1
    if rand not in numbers:
        print(lines[rand - 1].strip())
        numbers.append(rand)
