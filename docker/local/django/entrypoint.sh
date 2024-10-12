#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python << END
import sys
import time
import psycopg2
suggest_uncoverable_after = 30
start = time.time()
while True:
    try:
        psycopg2.connect(
        db_name = ${POSTGRES_DB},
        user = ${POSTGRES_USER},
        password = ${POSTGRES_PASSWORD},
        port = ${POSTGRES_PORT},
        host = ${POSTGRES_HOST}
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Watitng For Postgres To Become Available...\n")
        if time.time() - start > suggest_uncoverable_after:
            sys.stderr.write("This Is Taking Longer Than Excepcted, The Following Exception May Be An Indicative Of An Error '{}' \n ".format(error))
            sleep(1)
END

>&2 echo "PostgreSQL Is Available" 
exec "$@"