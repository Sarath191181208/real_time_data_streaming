import datetime
import json
from airflow.decorators import task, dag
from kafka import KafkaProducer
from airflow import DAG

import six
import sys
# https://stackoverflow.com/questions/77287622/modulenotfounderror-no-module-named-kafka-vendor-six-moves-in-dockerized-djan
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from data_generator import generate_fake_user

today = datetime.datetime.now()
SECONDS = 1
default_args = {
    "owner": "airscholar",
    "start_date": today,
}

producer = KafkaProducer(bootstrap_servers="localhost:9092", max_block_ms=10_000*SECONDS)

@task(task_id="stream_data")
def stream_data():
    for _ in range(100):
        user = generate_fake_user()
        data = json.dumps(user, default=str).encode("utf-8")
        producer.send("user_data", value=data)

@dag(dag_id="stream_data", default_args=default_args, schedule_interval="@daily")
def dag_service():
    stream_data()

