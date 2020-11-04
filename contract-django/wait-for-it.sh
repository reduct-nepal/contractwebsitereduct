#!/bin/sh
# wait-for-postgres.sh

set -e
  
host="$DATABASE_HOST"
shift
cmd="$@"
  
until PGPASSWORD=$POSTGRES_PASSWORD /usr/lib/postgresql/13/bin/psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
  
>&2 echo "Postgres is up - executing command"

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations main --noinput 
python manage.py migrate --noinput 

exec $cmd
