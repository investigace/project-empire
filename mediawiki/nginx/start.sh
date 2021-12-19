#!/bin/bash

export NGINX_SERVER_NAME=${DOMAIN}
export NGINX_DEFAULT_HOST=${DOMAIN}

export NGINX_SSL_CERTIFICATE="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
export NGINX_SSL_CERTIFICATE_KEY="/etc/letsencrypt/live/${DOMAIN}/privkey.pem"

if [ ! -f "$NGINX_SSL_CERTIFICATE" ]; then
  export NGINX_SSL_CERTIFICATE="/etc/ssl/certs/localhost-selfsigned.crt"
  export NGINX_SSL_CERTIFICATE_KEY="/etc/ssl/certs/localhost-selfsigned.key"
fi

envsubst '$NGINX_SERVER_NAME,$NGINX_DEFAULT_HOST,$NGINX_SSL_CERTIFICATE,$NGINX_SSL_CERTIFICATE_KEY' < /tmp/default.conf > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'
