#!/usr/bin/env bash

clone='git clone --depth=1'

repositories=(
  "https://github.com/neoclide/coc.nvim.git"
  "https://github.com/Yggdroot/indentLine.git"
  "https://github.com/tpope/vim-commentary.git"
  "https://github.com/iamcco/markdown-preview.nvim.git"
  "https://github.com/preservim/nerdtree.git"
  "https://github.com/editorconfig/editorconfig-vim.git"
  "https://github.com/tpope/vim-surround.git"
  "https://github.com/mattn/emmet-vim.git"
  "https://github.com/vim-airline/vim-airline.git"
  "https://github.com/tpope/vim-fugitive.git"
  "https://github.com/ryanoasis/vim-devicons.git"
  "https://github.com/junegunn/fzf.git"
  "https://github.com/sheerun/vim-polyglot.git"
  "https://github.com/junegunn/fzf.vim.git"
)

cd ~/.vim/pack/vendor/start/
for repository in "${repositories[@]}"; do
  $clone "$repository"
done

