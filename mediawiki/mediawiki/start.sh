#!/bin/bash

# When LocalSettings.php is missing, we treat it like MediaWiki was not
# installed yet
if [ ! -f "/opt/mediawiki_shared/LocalSettings.php" ]; then

  # Initializes MediaWiki in database and generates default LocalSettings.php
  php maintenance/install.php \
    --server="${SCHEME}://${DOMAIN}" \
    --dbuser=${MYSQL_USER} \
    --dbpass=${MYSQL_PASSWORD} \
    --dbname=${MYSQL_DATABASE} \
    --dbserver=db \
    --lang=${WIKI_LANG} \
    --pass=${WIKI_ADMIN_PASSWORD} \
    --scriptpath="" \
    "${WIKI_NAME}" \
    "${WIKI_ADMIN_USER}"

  # Enable file uploads
  sed -i 's/\$wgEnableUploads.*/\$wgEnableUploads = true;/g' /opt/mediawiki_shared/LocalSettings.php

  # Disable PHP cache
  sed -i 's/\$wgMainCacheType.*/\$wgMainCacheType = CACHE_NONE;/g' /opt/mediawiki_shared/LocalSettings.php

  # Change the emails
  sed -i "s/\$wgEmergencyContact.*/\$wgEmergencyContact = \"${ADMIN_EMAIL}\";/g" /opt/mediawiki_shared/LocalSettings.php
  sed -i "s/\$wgPasswordSender.*/\$wgPasswordSender = \"${ADMIN_EMAIL}\";/g" /opt/mediawiki_shared/LocalSettings.php

  # TODO: add default Common.css
  # TODO: add default Main page content
  # TODO: add default empire summary table
fi

apache2-foreground
