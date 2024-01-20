#!/usr/bin/env bash

read -r lines columns < <(stty size)
tmux new -d -x "$columns" -y "$(( lines - 1 ))" 2> /dev/null

tmux splitw -d -l 33%
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
    1.2 1.3
    2.0 2.1 2.2 2.3
  )

  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" "cd $HOME" C-m
  done

  path="$(realpath "$1")"

  # shellcheck source=/dev/null
  source "$HOME/scripts/project-scripts.bash"
  "${path//\//_}"

  lastModifiedFile="$(basename "$(find "$path" -maxdepth 1 -path './.git' -prune -o -printf '%T@ %p\n' | sort -n | tail -1 | awk '{ print $2 }')")"
  if [[ $lastModifiedFile == 'Session.vim' ]]; then
    tmux send 'nvim -S' C-m
  else
    tmux send 'nvim .' C-m
  fi
fi

tmux bind b switch-client -T firstWindowBindings

tmux bind -T firstWindowBindings a "joinp -h -s 0.1 -t 0.0"
tmux bind -T firstWindowBindings b "selectl main-horizontal; resizep -t 0.0 -y 67%"

tmux bind -T firstWindowBindings c "joinp -h -s 0.2 -t 0.0"
tmux bind -T firstWindowBindings d "joinp -h -s 0.1 -t 0.2"

tmux bind -T firstWindowBindings e "joinp -h -s 0.3 -t 0.0"
tmux bind -T firstWindowBindings f "joinp -h -s 0.1 -t 0.3"

tmux a

