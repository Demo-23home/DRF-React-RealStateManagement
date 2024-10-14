#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python << END
import sys
import time
import psycopg2
from time import sleep

suggest_uncoverable_after = 30
start = time.time()
while True:
    try:
        psycopg2.connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            port="${POSTGRES_PORT}",
            host="${POSTGRES_HOST}"
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Waiting For Postgres To Become Available...\n")
        if time.time() - start > suggest_uncoverable_after:
            sys.stderr.write(f"This is taking longer than expected. The following exception may be an indicator of an error: '{error}'\n")
            sleep(1)
END

>&2 echo "PostgreSQL Is Available" 
exec "$@"
