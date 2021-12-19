#!/bin/bash

php maintenance/install.php --server="https://${DOMAIN}" --dbuser=${MYSQL_USER} --dbpass=${MYSQL_PASSWORD} --dbname=${MYSQL_DATABASE} --dbserver=db --lang=${WIKI_LANG} --pass=${WIKI_ADMIN_PASSWORD} "${WIKI_NAME}" "${WIKI_ADMIN_USER}"

apache2-foreground
