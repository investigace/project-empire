#!/bin/bash

# Recreate /data directory
echo "Clearing /data directory"
rm -rf /data
mkdir -p /data

echo "Doing MariaDB database dump to /data"
mysqldump -h db -u ${MYSQL_USER} -p${MYSQL_PASSWORD} --databases ${MYSQL_DATABASE} > /data/mariadb-dump.sql

echo "Copying contents of mediawiki_shared to /data"
cp -r /mediawiki_shared /data/

# Default storage class to standard if not provided
S3_STORAGE_CLASS=${S3_STORAGE_CLASS:-STANDARD}

# Generate file name for tar
FILE_NAME=/tmp/empire-backup-`date "+%Y-%m-%d_%H-%M-%S"`.tar.gz

echo "Creating archive"
tar -zcvf $FILE_NAME /data

echo "Uploading archive to S3 [$FILE_NAME, storage class - $S3_STORAGE_CLASS]"
aws s3 cp --storage-class $S3_STORAGE_CLASS $FILE_NAME $BACKUP_S3_BUCKET_URL

echo "Removing local archive"
rm $FILE_NAME

echo "Done"
