#!/bin/bash

if [ ! "$BACKUP_ENABLE" == "true" ]; then
  echo "Backup to S3 is not enabled, not creating crontab"
else
  echo "Backup to S3 enabled, creating crontab"

  # Run every day at 4am
  echo -e "0 4 * * * /backup.sh\n" > /etc/crontabs/root
fi

echo "Starting crond"
crond -f
