#!/usr/bin/env bash

clone='git clone --depth=1'

repositories=(
  "git@github.com:neoclide/coc.nvim.git"
  "git@github.com:Yggdroot/indentLine.git"
  "git@github.com:tpope/vim-commentary.git"
  "git@github.com:iamcco/markdown-preview.nvim.git"
  "git@github.com:ctrlpvim/ctrlp.vim.git"
  "git@github.com:preservim/nerdtree.git"
  "git@github.com:editorconfig/editorconfig-vim.git"
  "git@github.com:tpope/vim-surround.git"
  "git@github.com:mattn/emmet-vim.git"
  "git@github.com:vim-airline/vim-airline.git"
  "git@github.com:tpope/vim-fugitive.git"
  "git@github.com:ryanoasis/vim-devicons.git"
  "git@github.com:junegunn/fzf.git"
  "git@github.com:sheerun/vim-polyglot.git"
  "git@github.com:junegunn/fzf.vim.git"
)

cd ~/.vim/pack/vendor/start/
for repository in "${repositories[@]}"; do
  $clone "$repository"
done

