#!/bin/bash

path="$(realpath "$1")"
basename="$(basename "$path")"
sessionName="${basename:0:6}"

cd || exit 1
tmux new-session -d -s "$sessionName"

tmux send-keys -t "$sessionName":0 "cd $path" C-m
if [ -f "$path/Session.vim" ]; then
  tmux send-keys -t "$sessionName":0 'vim -S' C-m
else
  tmux send-keys -t "$sessionName":0 'vim .' C-m
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

tmux attach -t "$sessionName":0.0
