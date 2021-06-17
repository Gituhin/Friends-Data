mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "[theme]
base="dark"
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
