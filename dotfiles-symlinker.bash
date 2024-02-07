#!/usr/bin/env bash

set -e
shopt -s dotglob
for file in "$HOME"/dotfiles/* ; do
  [[ -f $file ]] && [[ $(basename "$file") != "init.lua" ]] && [[ $(basename \
    "$file") != README.md ]] && ln -sf "$file" "$HOME/"
done

ln -sf "$HOME/dotfiles/init.lua" "$HOME/.config/nvim/"

