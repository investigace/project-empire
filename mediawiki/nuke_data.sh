#!/usr/bin/env bash

CURRENT_DIR=$(dirname "$1")

MEDIAWIKI_LOCAL_SETTINGS_PHP=$(realpath $CURRENT_DIR/mediawiki/shared/LocalSettings.php)
MEDIAWIKI_IMAGES=$(realpath $CURRENT_DIR/mediawiki/shared/images)
MARIADB_DATA=$(realpath $CURRENT_DIR/mariadb/data)

echo ""
echo "Are you sure you want to nuke all data of running mediawiki here?"
echo "Will remove:"
echo "  - $MEDIAWIKI_LOCAL_SETTINGS_PHP"
echo "  - $MEDIAWIKI_IMAGES (contents of directory)"
echo "  - $MARIADB_DATA (contents of directory)"
echo ""

read -p "Confirm nuke (y/n)?" choice
case "$choice" in 
  y|Y ) ;;
  n|N ) echo "Doing nothing"; exit 0;;
  * ) echo "Doing nothing"; exit 0;;
esac

rm $MEDIAWIKI_LOCAL_SETTINGS_PHP

rm -rf $MEDIAWIKI_IMAGES/*
touch $MEDIAWIKI_IMAGES/.gitkeep

rm -rf $MARIADB_DATA/*
touch $MARIADB_DATA/.gitkeep

echo "Nuke done"
