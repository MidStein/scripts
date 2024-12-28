#!/usr/bin/env bash
rm -fr public src/assets src/*.css

sed -i '/vite\.svg/d' index.html
sed -i 's/Vite \+ React//' index.html

if [[ -f src/App.tsx ]]; then
  sed -i \
    's/\. --ext ts,tsx --report-unused-disable-directives --max-warnings 0/--ext .ts,.tsx ./' \
    package.json
  sed -i '/index\.css/d' src/main.tsx

  sed -i '/reactLogo/d' src/App.tsx
  sed -i '/viteLogo/d' src/App.tsx
  sed -i '/App\.css/d' src/App.tsx
else
  sed -i \
    's/\. --ext js,jsx --report-unused-disable-directives --max-warnings 0/--ext .js,.jsx ./' \
    package.json
  sed -i '/index\.css/d' src/main.jsx

  sed -i '/reactLogo/d' src/App.jsx
  sed -i '/viteLogo/d' src/App.jsx
  sed -i '/App\.css/d' src/App.jsx
fi

npm i && npm i -D \
  eslint-config-airbnb-base \
  prettier \
  eslint-config-prettier \
  prop-types
