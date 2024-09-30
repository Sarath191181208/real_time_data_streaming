#!/bin/bash
set -e

# installing the pipenv 
pip install pipenv 

cd /opt/airflow
echo $PWD
# installing modules using pipenv
pipenv install --system --deploy --ignore-pipfile

# init the airflow db
if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init && \
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
fi

$(command -v airflow) db upgrade
exec airflow scheduler &
exec airflow webserver
