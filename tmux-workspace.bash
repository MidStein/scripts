#!/usr/bin/env bash

read -r lines columns < <(stty size)

if [[ ! "$1" ]]; then
  cd "$HOME" || exit
else
  if [[ -d "$1" ]]; then
    path="$(realpath "$1")"
  else
    path=$(zoxide query "$1") || exit
  fi
  cd $path || exit
fi
tmux new -d -x "$columns" -y "$(( lines - 1 ))" 2> /dev/null

tmux splitw -d -l 33%
tmux splitw -d -h -t 0.1
tmux resizep -Z -t 0.0

tmux neww -d
tmux splitw -d -l 5% -t 1.0
tmux splitw -h -t 1.0
tmux selectp -t 1.0
tmux splitw -d -h -t 1.2

tmux neww -c "$HOME" -d
tmux splitw -c "$HOME" -d -l 5% -t 2.0
tmux splitw -c "$HOME" -h -t 2.0
tmux selectp -t 2.0
tmux splitw -c "$HOME" -d -h -t 2.2

if [[ ! "$1" ]]; then
  tmux send 'nvim' C-m
else
  # shellcheck source=/dev/null
  source "$HOME/scripts/directory-functions.bash"
  pathFromHome=${path#"$HOME/"}
  functionName=${pathFromHome//\//_}
  [[ $(type -t "$functionName") == function ]] && $functionName
  tmux set status-right "$(basename $path)"

  lastModifiedFile="$(basename "$(find "$path" -maxdepth 1 -path './.git' \
    -prune -o -printf '%T@ %p\n' | sort -n | tail -1 | awk '{ print $2 }')")"
  if [[ $lastModifiedFile == 'Session.vim' ]]; then
    tmux send 'nvim -S' C-m
  else
    tmux send '[[ -f Session.vim ]] && rm Session.vim; nvim .' C-m
  fi
fi

tmux bind b switch-client -T firstWindowBindings

tmux bind -T firstWindowBindings a 'joinp -h -s 0.1 -t 0.0'
tmux bind -T firstWindowBindings z \
  'selectl main-horizontal; resizep -t 0.0 -y 67%'

tmux bind -T firstWindowBindings b 'joinp -h -s 0.2 -t 0.0'
tmux bind -T firstWindowBindings y 'joinp -h -s 0.1 -t 0.2'

tmux bind -T firstWindowBindings c 'joinp -h -s 0.3 -t 0.0'
tmux bind -T firstWindowBindings x 'joinp -h -s 0.1 -t 0.3'

tmux bind e 'swapp -t .3'

tmux a
