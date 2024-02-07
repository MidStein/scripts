function _home_deepak_code-lpu_int253_mysite() {
  paneNums=(
    0.0 0.1 0.2 0.3
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" "source $HOME/code-lpu/int253/mysite/.venv/bin/activate" C-m
  done

  tmux send -t 0.1 '# ./manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}

function _home_deepak_code-lpu_int253_class_project() {
  paneNums=(
    0.0 0.1 0.2 0.3
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" "source $HOME/code-lpu/int253/class_project/.venv/bin/activate" C-m
  done

  tmux send -t 0.1 './manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}

function _home_deepak_code-lpu_int253_regular_expressions() {
  paneNums=(
    0.0 0.1 0.2 0.3
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" "source $HOME/code-lpu/int253/regular_expressions/.venv/bin/activate" C-m
  done
}

function _home_deepak_code_latex_jake() {
  tmux send -t 0.1 'make all' C-m
}
