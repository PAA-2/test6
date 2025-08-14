#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Usage: restore.sh <timestamp>"; exit 1; fi
TS=$1
gunzip -c backups/db-$TS.sql.gz | psql $DATABASE_URL
tar -xzf backups/storage-$TS.tar.gz
