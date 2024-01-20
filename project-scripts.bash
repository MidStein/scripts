function _home_deepak_code-lpu_int253_mysite() {
  paneNums=(
    0.0 0.1 0.2 0.3
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" "source $HOME/.virtualenvs/mysite/bin/activate" C-m
  done

  tmux send -t 0.0 "let g:ctrlp_custom_ignore = '\v[\/](\.git|__pycache__)$'"
  tmux send -t 0.1 '# ./manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}
function _home_deepak_code-lpu_int253_class_project() {
  paneNums=(
    0.0 0.1 0.2 0.3
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" "source $HOME/.virtualenvs/class_project/bin/activate" C-m
  done

  tmux send -t 0.0 "let g:ctrlp_custom_ignore = '\v[\/](\.git|__pycache__)$'"
  tmux send -t 0.1 './manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}
function _home_deepak_code_latex_jake() {
  tmux send -t 0.1 'make all'
}
