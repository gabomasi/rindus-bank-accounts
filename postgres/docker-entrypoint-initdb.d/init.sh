#!/bin/bash
psql -U postgres -c "CREATE USER $DB_USER PASSWORD '$DB_PASS'"
psql -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER"

psql -U postgres -c  "ALTER ROLE $DB_USER superuser"
psql -U "$DB_USER" -c "CREATE EXTENSION postgis"
psql -U postgres -c  "ALTER ROLE $DB_USER nosuperuser"
