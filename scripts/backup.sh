#!/bin/bash
set -e
TS=$(date +%Y%m%d_%H%M)
mkdir -p backups
pg_dump $DATABASE_URL | gzip > backups/db-$TS.sql.gz
tar -czf backups/storage-$TS.tar.gz storage/
find backups -type f -mtime +${BACKUP_RETENTION_DAYS:-7} -delete
