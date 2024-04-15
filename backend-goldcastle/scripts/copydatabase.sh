#!/bin/bash

# Define variables
DB_HOST="postgres"  # Assuming "postgres" is the hostname of your PostgreSQL container
DB_PORT="5432"       # Assuming the default PostgreSQL port
DB_NAME="goldcastle"
DB_USER="esse"
DB_PASSWORD="96509035"
BACKUP_DIR="/app/databases/backups"
BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +"%Y-%m-%d_%H-%M-%S").sql"

# Set the PGPASSWORD environment variable
export PGPASSWORD="$DB_PASSWORD"

# Create the backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Run pg_dump command with hostname, port, username, and password
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

