#!/usr/bin/env bash

dotfiles=$(find "$HOME/dotfiles/" -maxdepth 1 -type f)
for dotfile in $dotfiles; do
  if [[ "$(basename "$dotfile")" = "init.lua" ]]; then
    rm "$HOME/.config/nvim/init.lua"
    ln -s "$dotfile" "$HOME/.config/nvim/init.lua"
    continue
  fi
  rm "$HOME/$(basename "$dotfile")"
  ln -s "$dotfile" "$HOME/$(basename "$dotfile")"
done

