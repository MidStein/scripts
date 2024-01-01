#!/bin/bash

if [ ! "$1" ]; then
  exit 1
fi

path="$(realpath "$1")"
basename="$(basename "$path")"
sessionName="${basename:0:8}"

tmux new-session -d -s "$sessionName"

lastModifiedFile="$(basename "$(find "$path" -maxdepth 1 -printf '%T@ %p\n' | sort -n | tail -1 | cut -d " " -f 2)")"

tmux send-keys -t "$sessionName":0 "cd $path" C-m
if [[ $lastModifiedFile = "Session.vim" ]]; then
  tmux send-keys -t "$sessionName":0 'nvim -S' C-m
else
  tmux send-keys -t "$sessionName":0 'nvim .' C-m
fi
tmux split-window
tmux resize-pane -t "$sessionName":0.1 -y 10%
tmux send-keys -t "$sessionName":0.1 "cd $path" C-m 'make' C-m

tmux new-window -t "$sessionName":1
tmux send-keys "cd $path" C-m
tmux split-window -h
tmux send-keys "cd temp" C-m
tmux resize-pane -t "$sessionName":1.1 -x 15%
tmux select-pane -t "$sessionName":1.0
tmux resize-pane -t "$sessionName":1.0 -Z

tmux attach -t "$sessionName":0.0
