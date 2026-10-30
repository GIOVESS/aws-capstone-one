FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
# Writes config.js from the API_URL env var at container start
COPY 40-config.sh /docker-entrypoint.d/40-config.sh
RUN chmod +x /docker-entrypoint.d/40-config.sh

EXPOSE 80
