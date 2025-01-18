#!/bin/bash
# wait_for_db.sh

until nc -z -v -w30 $DB_HOST 5432; do
  echo "Waiting for database connection..."
  sleep 1
done
echo "Database is up, continuing..."
