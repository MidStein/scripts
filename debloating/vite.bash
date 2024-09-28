#!/usr/bin/env bash
rm -rf public src/assets src/*.css

sed -i \
  's/ --report-unused-disable-directives --max-warnings 0//' \
  package.json
sed -i '/vite\.svg/d' index.html
sed -i 's/Vite \+ React//' index.html
sed -i '/index\.css/d' src/main.jsx

sed -i '/reactLogo/d' src/App.jsx
sed -i '/viteLogo/d' src/App.jsx
sed -i '/App\.css/d' src/App.jsx

npm i && npm i -D \
  eslint-config-airbnb-base \
  prettier \
  eslint-config-prettier \
  prop-types
