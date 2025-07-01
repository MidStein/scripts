#!/usr/bin/env bash

set -e

for_home=(.bashrc .aliases.bash .inputrc)
for_config=(curlrc alacritty git nvim sqlite3 tmux zathura)

for file in "${for_home[@]}"; do
  [[ -e $file ]] && ln -sf "$HOME/dotfiles/$file" "$HOME/"
done
for file in "${for_config[@]}"; do
  [[ -e $file ]] && ln -sf "$HOME/dotfiles/$file" "$HOME/.config"
done
