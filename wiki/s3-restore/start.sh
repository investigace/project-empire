#!/bin/bash

echo "Finding latest backup file"
LATEST_BACKUP_FILE=`aws s3 ls $BACKUP_S3_BUCKET_URL --recursive | sort | tail -n 1 | awk '{print $4}'`
echo "Found: $LATEST_BACKUP_FILE"

echo "Downloading $LATEST_BACKUP_FILE"
aws s3 cp $BACKUP_S3_BUCKET_URL$LATEST_BACKUP_FILE /backup.tar.gz

echo "Extracting backup to /data"
tar -zxvf /backup.tar.gz

echo "Restoring MariaDB database"
mysql -h db -u $MYSQL_USER -p$MYSQL_PASSWORD < /data/mariadb-dump.sql

echo "Coping mediawiki_shared"
cp -r /data/mediawiki_shared/* /mediawiki_shared/

echo "Cleaning up /data"
rm -rf /data

echo "Done"
