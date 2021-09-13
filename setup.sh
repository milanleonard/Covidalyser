mkdir -p .streamlit/
echo -e "\
[server]\n\
headless = true\n\
port = $PORT\n\
" > .streamlit/config.toml
