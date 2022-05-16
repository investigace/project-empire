#!/bin/bash

export DEFAULT_DOMAIN=${DOMAIN}
export REDIRECT_DOMAIN=${REDIRECT_DOMAIN}

export DEFAULT_SSL_CERTIFICATE="/etc/letsencrypt/live/${DEFAULT_DOMAIN}/fullchain.pem"
export DEFAULT_SSL_CERTIFICATE_KEY="/etc/letsencrypt/live/${DEFAULT_DOMAIN}/privkey.pem"

if [ ! -f "$DEFAULT_SSL_CERTIFICATE" ]; then
  export DEFAULT_SSL_CERTIFICATE="/etc/ssl/certs/localhost-selfsigned.crt"
  export DEFAULT_SSL_CERTIFICATE_KEY="/etc/ssl/certs/localhost-selfsigned.key"
fi

export REDIRECT_SSL_CERTIFICATE="/etc/letsencrypt/live/${REDIRECT_DOMAIN}/fullchain.pem"
export REDIRECT_SSL_CERTIFICATE_KEY="/etc/letsencrypt/live/${REDIRECT_DOMAIN}/privkey.pem"

if [ ! -f "$REDIRECT_SSL_CERTIFICATE" ]; then
  export REDIRECT_SSL_CERTIFICATE="/etc/ssl/certs/localhost-selfsigned.crt"
  export REDIRECT_SSL_CERTIFICATE_KEY="/etc/ssl/certs/localhost-selfsigned.key"
fi

envsubst '$DEFAULT_DOMAIN,$DEFAULT_SSL_CERTIFICATE,$DEFAULT_SSL_CERTIFICATE_KEY' < /tmp/default.conf > /etc/nginx/conf.d/default.conf

if [ ! -z "$REDIRECT_DOMAIN" ]; then
  envsubst '$DEFAULT_DOMAIN,$REDIRECT_DOMAIN,$REDIRECT_SSL_CERTIFICATE,$REDIRECT_SSL_CERTIFICATE_KEY' < /tmp/redirect.conf > /etc/nginx/conf.d/redirect.conf
else
  # If we are not using the configuration for redirect domain, make
  # sure that there is not the old configuration file
  rm -f /etc/nginx/conf.d/redirect.conf
fi

# Reloading configuration periodically so we are loading the newly
# obtained certificates by certbot
while :
do
    sleep 6h
    nginx -s reload
done &

nginx -g 'daemon off;'
