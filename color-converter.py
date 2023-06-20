#!/usr/bin/env python3
import sys
from PIL import ImageColor
import matplotlib.colors

if len(sys.argv) - 1 == 1:
    hex = sys.argv[1]
    print(ImageColor.getcolor(hex, 'RGB'))
elif len(sys.argv) - 1 == 3:
    r = int(sys.argv[1]) / 255
    g = int(sys.argv[2]) / 255
    b = int(sys.argv[3]) / 255
    rgb = (r, g, b)
    print(matplotlib.colors.to_hex(rgb))

