#!/bin/bash

# When LocalSettings.php is missing, we treat it like MediaWiki was not
# installed yet
if [ ! -f "/opt/mediawiki_shared/LocalSettings.php" ]; then

  install_pages_dir="/root/install_pages/${INSTALL_WIKI_LANG}"

  if [ ! -d $install_pages_dir ]; then
    echo "Directory of install pages $install_pages_dir does not exist, probably unknown INSTALL_WIKI_LANG setting?"
    exit 1
  fi

  # Initializes MediaWiki in database and generates default LocalSettings.php
  php maintenance/install.php \
    --server="${SCHEME}://${DOMAIN}" \
    --dbuser=${MYSQL_USER} \
    --dbpass=${MYSQL_PASSWORD} \
    --dbname=${MYSQL_DATABASE} \
    --dbserver=db \
    --lang=${INSTALL_WIKI_LANG} \
    --pass=${INSTALL_WIKI_ADMIN_PASSWORD} \
    --scriptpath="" \
    "${INSTALL_WIKI_NAME}" \
    "${INSTALL_WIKI_ADMIN_USER}"

  # Enable file uploads
  sed -i 's/\$wgEnableUploads.*/\$wgEnableUploads = true;/g' /opt/mediawiki_shared/LocalSettings.php

  # Disable PHP cache
  sed -i 's/\$wgMainCacheType.*/\$wgMainCacheType = CACHE_NONE;/g' /opt/mediawiki_shared/LocalSettings.php

  # Change the emails
  sed -i "s/\$wgEmergencyContact.*/\$wgEmergencyContact = \"${ADMIN_EMAIL}\";/g" /opt/mediawiki_shared/LocalSettings.php
  sed -i "s/\$wgPasswordSender.*/\$wgPasswordSender = \"${ADMIN_EMAIL}\";/g" /opt/mediawiki_shared/LocalSettings.php

  # Change logo
  sed -i "s/\$wgLogos.*/\$wgLogos = \['1x'=>\$wgResourceBasePath \. '\/project_empire_wiki_logo.svg'\];/g" /opt/mediawiki_shared/LocalSettings.php

  # Enable Iframe extension
  echo "wfLoadExtension( 'Iframe' );" >> /opt/mediawiki_shared/LocalSettings.php
  echo "\$wgIframe['server']['${DOMAIN}'] = [ 'scheme' => '${SCHEME}', 'domain' => '${DOMAIN}' ];" >> /opt/mediawiki_shared/LocalSettings.php

  # Enable EmbedVideo extension
  echo "wfLoadExtension( 'EmbedVideo' );" >> /opt/mediawiki_shared/LocalSettings.php

  # Install pages
  for page_path in "$install_pages_dir"/*
  do
    page_name=$(basename $page_path)

    # We keep the page names urlencoded so we can have spaces or colons in their name
    page_name=$(echo $page_name | php -R 'echo urldecode($argn)."\n";')

    php maintenance/edit.php \
      -s "Project Empire wiki installation" \
      "$page_name" \
      < $page_path
  done
fi

apache2-foreground
