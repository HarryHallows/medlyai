# !/usr/bin/env bash
set -e

# wait for db
until pg_isready -h db -p 5432 -U postgres; do
    echo "Waiting for db..."
    sleep 1
done


# create tables
python -c "from app.db import Base, engine; Base.metadata.create_all(bind=engine)"

# run migration
python scripts/migrate.py

# start API
uvicorn app.main:app --host 0.0.0.0 --port 8000
