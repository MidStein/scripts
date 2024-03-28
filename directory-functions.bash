function code-lpu_int253_mysite() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done

  tmux send -t 0.1 '#./manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}

function code-lpu_int253_class_project() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done

  tmux send -t 0.1 './manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}

function code-lpu_int253_regular_expressions() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done
}

function code_javascript_odin_react_where-s-waldo() {
  tmux send -t 0.1 'npm start' C-m
}

function code_javascript_odin_javascript_weather-app() {
  tmux send -t 0.1 'wslpath -w index.html | clip' C-m
}

function code_javascript_odin_javascript_todo-list() {
  tmux send -t 0.1 'wslpath -w docs/index.html | clip' C-m
  tmux send -t 0.1 'npx webpack watch -o docs' C-m
}

function code_javascript_fso_part4_blog-list() {
  variables="\
    header='Content-Type: application/json';
    url='localhost:3003/api/blogs'\
  "
  for pane in 0.1 0.2 1.0 1.1 1.2 1.3; do
    tmux send -t "$pane" "$variables" C-m
  done
}

function code_javascript_odin_react_shopping-cart() {
  tmux send -t 0.1 'npm start' C-m
}

function code_python_flask_myproject() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done
}

function code_python_flask_flask-tutorial() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done

  tmux send -t 0.1 'flask -A flaskr run --debug'
}

function python_websockets() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done

  tmux send -t 0.1 '#./manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}

function code-lpu_int253_class_project() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done

  tmux send -t 0.1 './manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}

function code-lpu_int253_regular_expressions() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done
}

function code_javascript_odin_react_where-s-waldo() {
  tmux send -t 0.1 'npm start' C-m
}

function code_javascript_odin_javascript_weather-app() {
  tmux send -t 0.1 'wslpath -w index.html | clip' C-m
}

function code_javascript_odin_javascript_todo-list() {
  tmux send -t 0.1 'wslpath -w docs/index.html | clip' C-m
  tmux send -t 0.1 'npx webpack watch -o docs' C-m
}

function code_javascript_fso_part4_blog-list() {
  variables="\
    header='Content-Type: application/json';
    url='localhost:3003/api/blogs'\
  "
  for pane in 0.1 0.2 1.0 1.1 1.2 1.3; do
    tmux send -t "$pane" "$variables" C-m
  done
}

function code_javascript_odin_react_shopping-cart() {
  tmux send -t 0.1 'npm start' C-m
}

function job-hunt() {
  tmux killp -t 0.1
  tmux resizep -t 0.1 -x 50%
  tmux resizep -t 1.0 -x 60%
  tmux send -t 1.0 'sqlite3 job-hunt.sqlite' C-m
  tmux send -t 1.0 'SELECT * from drive ORDER BY id DESC LIMIT 20\;' C-m
}

function code_python_flask_myproject() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done
}

function code_python_flask_flask-tutorial() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done

  tmux send -t 0.1 'flask -A flaskr run --debug'
}

function code_python_websockets() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done
}

function code-jobs_instahyre() {
  paneNums=(
    0.0 0.1 0.2
    1.0 1.1 1.2 1.3
  )
  for paneNum in "${paneNums[@]}"; do
    tmux send -t "$paneNum" \
      "source .venv/bin/activate" C-m
  done

  tmux send -t 0.1 './manage.py runserver' C-m
  tmux send -t 1.1 './manage.py shell' C-m
}
