# Scripts

Automation scripts and helper tools.

---

### Files

- [autohotkey.ahk](#autohotkeyahk)
- [color-converter\.py](#color-converterpy)
- [directory-functions.bash](#directory-functionsbash)
- [dotfiles-symlinker.bash](#dotfiles-symlinkerbash)
- [rng\.py](#rngpy)
- [tmux.bash](#tmuxbash)

---

## autohotkey\.ahk

An autohotkey script for Windows. The day anti cheat software start working
properly on Linux, will be the day when this script gets deleted.
This script shows a small menu which has an input box and a list of tasks along
with alphabets character before them. On entering an alphabet in the input, the
associated task runs.

- CursorLeft. Puts the mouse cursor on the left. I rarely use the mouse.
- ClickCenterRight. Useful for those websites that steal focus from scrolling
area making keyboard navigation difficult
- GameMode. Change Windows power mode to best performance. Turn on eSports
mode on AMD Radeon settings. Close other applications.
- EntertainMode. Open media folder. Maximize brightness.
- MusicMode. Open spotify on chrome and put focus on search bar.

## color-converter\.py

Tool to convert HEX to RGB color code and vice versa. Uses python's PIL and
matplotlib libraries.

```python
#!/usr/bin/env python3

import sys
from PIL import ImageColor
from matplotlib import colors

if len(sys.argv) - 1 == 1:
    hex = sys.argv[1]
    print(ImageColor.getcolor(hex, 'RGB'))
elif len(sys.argv) - 1 == 3:
    r = int(sys.argv[1]) / 255
    g = int(sys.argv[2]) / 255
    b = int(sys.argv[3]) / 255
    rgb = (r, g, b)
    print(colors.to_hex(rgb))
```

## directory-functions\.bash

An extension of [tmux.bash](#tmuxbash). This file stores custom functions based
on the directory that was passed to tmux.bash.

## dotfiles-symlinker\.bash

```bash
$ # Whoops, ran find -type f -maxdepth 1 -delete on the wrong directory ($HOME)
$ # , or Oh, I just installed this new linux distro, what am I ever gonna do?
$ git clone github.com/MidStein/dotfiles
$ git checkout suitableBranch
$ git clone github.com/MidStein/scripts
$ ./scripts/dotfiles-symlinker.bash
$
```

```bash
#!/usr/bin/env bash

set -e
shopt -s dotglob
for file in "$HOME"/dotfiles/* ; do
  [[ -f $file ]] && [[ $(basename "$file") != "init.lua" ]] && [[ $(basename \
    "$file") != README.md ]] && ln -sf "$file" "$HOME/"
done

ln -sf "$HOME/dotfiles/init.lua" "$HOME/.config/nvim/"
```

## rng\.py

Tool to generate multiple random numbers in a range. Uses python's secrets
library that generates cryptographically secure pseudo-random numbers unlike
python's random module.

```bash
$ # Can't decide out of 50 books in the shelf, which book to pick
$ ./rng.py --max 50
14

$ # avinash <CR> name already taken
$ # avinash56 <CR> name already taken
$ # avinash39 <CR> name already taken
$ # why are there so many avinash?! all two digits numbers are also taken
$ ./rng.py --min 100 --max 999
713
$ # avinash713 not taken. yay!

$ # You want to generate my password using a wordlist which needs me to throw a
$ # die 4 times. Problem is you do not have a die. Say no more.
$ rand=$(./rng.py --max 6 -c 4)
3 4 2 4
$ grep "$(echo "$rand" | tr -d ' ')" wordlist.txt | awk '{ print $2 }'
success
```

```python
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
```

## tmux\.bash

I have a well organized file system and I consider software project directories
an *office* for work in the hypothetical file system *building*. So, when I
have to do some kind of work, I go to the particular directory for it and run
this script that sets up tmux in that directory as the base.

No matter what the work, I keep the same layout of panes. Eg: First window has
one main pane running NeoVim, there are three panes below it. One runs
servers/compile commands. Another one I use to run project related commands that
need to be run in the same directory like git and file management commands. The
last one runs commands unrelated to the directory path.

According to the directory, this scripts runs a function that in turn runs some
custom scripts. These functions that store custom scripts for each directory, I
have put in [directory-functions.bash](#directory-functionsbash).

Since the layout stays the same, I also have custom bindings that move the pane
in the exact position and size I want. So, if the pane running the server shows
an error, with some simple key presses I can get that pane with the same size as
my editor. This way I can focus on these two panes in particular.

