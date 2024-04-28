#!/bin/sh
set -e

# Check if the database was initialized
if [ "${EFTDMS_DJANGO_BACKEND_INIT}" = "true" ]; then
    echo "Check if initialization is required ..."
    APPLIED_MIGRATIONS=$(python3 manage.py showmigrations | grep "\[X\]" | wc -l)
    if [ "${APPLIED_MIGRATIONS}" = "0" ]; then
        echo "No applied migrations. Initializing app ..."
        python3 manage.py migrate
    else
        echo "App already initialized. Skipping"
    fi
fi

# Migrate if desired
if [ "${EFTDMS_DJANGO_BACKEND_MIGRATE}" = "true" ]; then
    echo "Migrate ..."
    python3 manage.py migrate
fi

# Update static files in volume
echo "Sync static files to shared volume ..."
rm -rf "/mnt/backend_static/*"
cp -r "/app/static/." "/mnt/backend_static"

exec "$@"
