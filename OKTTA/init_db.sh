#!/bin/bash
set -e

# Ждем, пока база данных будет готова
until pg_isready -U "${POSTGRES_USER}"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 5
done

# Проверяем, существует ли база данных
if psql -U "${POSTGRES_USER}" -lqt | cut -d \| -f 1 | grep -qw "${POSTGRES_DB}"; then
  echo "Database ${POSTGRES_DB} already exists. Skipping data import."
else
  echo "Restoring database from dump..."
  psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -f /docker-entrypoint-initdb.d/data_db.sql
fi