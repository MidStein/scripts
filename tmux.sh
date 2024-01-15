#!/usr/bin/env bash

read -r lines columns < <(stty size)
if [[ "$1" ]]; then
  path="$(realpath "$1")"
  basename="$(basename "$path")"
  sessionName="${basename:0:8}"

  tmux new -d -s "$sessionName" -x "$columns" -y "$(( lines - 1 ))" 2> /dev/null
else
  tmux new -d -x "$columns" -y "$(( lines - 1 ))" 2> /dev/null
fi

tmux splitw -d -l 25%
tmux splitw -d -h -l 66% -t 0.1
tmux splitw -d -h -l 50% -t 0.2

tmux neww -d
tmux splitw -d -l 5% -t 1.0
tmux splitw -d -h -t 1.0
tmux splitw -d -h -t 1.2

tmux neww -d
tmux splitw -d -l 5% -t 2.0
tmux splitw -d -h -t 2.0
tmux splitw -d -h -t 2.2

if [[ ! "$1" ]]; then
  tmux send 'nvim' C-m
else
  paneNums=(
    0.3
    1.2 1.3
    2.0 2.1 2.2 2.3
  )

  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" "cd $HOME" C-m
  done

  # shellcheck source=/dev/null
  source "$HOME/scripts/project-scripts.sh"
  "${path//\//_}"

  lastModifiedFileTime="$(basename "$(find "$path" -maxdepth 1 -printf '%T@\n' | sort -n | tail -1)")"
  sessionFile="$HOME/.local/share/nvim/sessions/${path//\//_}"
  if [[ -f $sessionFile ]] && [[ $(stat -c %Y "$sessionFile") > "$lastModifiedFileTime" ]]; then
    tmux send "nvim -S $sessionFile" C-m
  else
    tmux send 'nvim .' C-m
  fi
fi

tmux bind b switch-client -T firstWindowBindings

tmux bind -T customBindings a "joinp -h -s 0.3 -t 0.0"
tmux bind -T customBindings b "joinp -h -s 0.1 -t 0.3"

tmux bind -T customBindings c "resizep -t 0.1 -x 5%;
  resizep -t  -x 47%"
tmux bind -T customBindings d "resizep -t 0.3 -x 5%;
  resizep -t 0.1 -x 47%"

tmux bind -T customBindings e 'selectl main-horizontal; resizep -t 0.1 -y 25%'

tmux a

