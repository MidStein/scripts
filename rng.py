#!/usr/bin/env python3

import secrets
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", type=int, help="minimum")
parser.add_argument("-M", type=int, help="maximum")
parser.add_argument("-c", type=int, help="count of random numbers")
parser.add_argument("-f", type=argparse.FileType('r'), help="file")
args = parser.parse_args()

if not args.f:
    min = args.m if args.m else 1
    if args.c:
        count = args.c
    elif args.M - min + 1 < 5:
        count = args.M - min + 1
    else:
        count = 5
    if count > args.M - min + 1:
        print(f"Range too small for generating {count} random numbers")
        exit()

    numbers = []
    while len(numbers) < count:
        rand = secrets.randbelow(args.M - min + 1) + min
        if rand not in numbers:
            print(rand, end=' ')
            numbers.append(rand)
    print()
else:
    with args.f as file:
        lines = file.readlines()
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
