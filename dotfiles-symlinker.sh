#!/usr/bin/env bash

dotfiles=$(find "$HOME/dotfiles/" -maxdepth 1 -type f)
for dotfile in $dotfiles; do
  rm "$HOME/$(basename "$dotfile")"
  ln -s "$dotfile" "$HOME/$(basename "$dotfile")"
done

