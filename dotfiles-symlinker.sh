#!/usr/bin/env bash

dotfiles=$(ls -A ~/dotfiles)
for dotfile in $dotfiles; do
  if [[ "$dotfile" != ".git" && "$dotfile" != ".gitignore" ]]; then
    if [[ ! ($(uname -s) == MINGW64_NT* && "$dotfile" == ".profile") ]]; then
      rm ~/"$dotfile"
      ln -s ~/dotfiles/"$dotfile" ~/"$dotfile"
    fi
  fi
done

