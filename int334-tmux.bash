#!/usr/bin/env bash

read -r lines columns < <(stty size)

path="$HOME/code-lpu/int334"
cd "$path" || exit
tmux new -d -s 'INT334' -x "$columns" -y "$(( lines - 1 ))" 2> /dev/null

tmux splitw -d -h
tmux splitw -c "$HOME" -d -t 0.1

tmux neww -d
tmux splitw -d -l 5% -t 1.0
tmux splitw -d -h -t 1.0
tmux splitw -d -h -t 1.2

tmux neww -c "$HOME" -d
tmux splitw -c "$HOME" -d -l 5% -t 2.0
tmux splitw -c "$HOME" -d -h -t 2.0
tmux splitw -c "$HOME" -d -h -t 2.2

lastModifiedFile="$(basename "$(find "$path" -maxdepth 1 -path './.git' \
  -prune -o -printf '%T@ %p\n' | sort -n | tail -1 | awk '{ print $2 }')")"
if [[ $lastModifiedFile == 'Session.vim' ]]; then
  tmux send 'nvim -S' C-m
else
  tmux send 'nvim .' C-m
fi

tmux a

