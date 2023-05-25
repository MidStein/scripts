#!/usr/bin/env python3
import sys
import secrets

c = int(sys.argv[2]) if len(sys.argv) > 2 else 1

for _ in range(c):
    print(secrets.randbelow(int(sys.argv[1])) + 1, end=' ')

print()

