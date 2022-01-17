#!/bin/bash

export DOMAINS_LIST="$DOMAIN"

if [ ! -z "$REDIRECT_DOMAIN" ]; then
  export DOMAINS_LIST="$DOMAIN $REDIRECT_DOMAIN"
fi

for loop_domain in ${DOMAINS_LIST}; do
  echo "Obtaining certificate for domain $loop_domain..."
  certbot certonly --webroot --webroot-path=/var/www/certbot --email $ADMIN_EMAIL --non-interactive --agree-tos --no-eff-email -d $loop_domain
done

while true; do
  certbot renew -q
  sleep 10h
done
