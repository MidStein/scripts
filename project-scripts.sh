function _home_deepak_code-lpu_int253_mysite() {
  paneNums=(
    0.0 0.1 0.2 0.3
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" "source $HOME/.virtualenvs/int253/bin/activate" C-m
  done
}
