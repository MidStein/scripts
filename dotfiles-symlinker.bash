#!/usr/bin/env bash

set -e

for file in "$HOME"/dotfiles/.*; do
  [[ -f $file ]] && ln -sf "$(realpath "$file")" "$HOME/"
done
for dir in "$HOME"/dotfiles/* ; do
  [[ "$(basename $file)" != README.md ]] && ln -sf "$(realpath "$file")" "$HOME/.config"
done
