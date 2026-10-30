#!/bin/sh
set -eu
cat > /usr/share/nginx/html/config.js <<CFG
window.APP_CONFIG = { apiUrl: "${API_URL:-}" };
CFG
echo "config.js written (apiUrl=${API_URL:-unset})"
