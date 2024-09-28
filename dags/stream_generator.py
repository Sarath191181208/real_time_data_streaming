import datetime
import json
from airflow.decorators import  dag
from airflow.operators.python import PythonOperator
from kafka import KafkaProducer

import six
import sys
# https://stackoverflow.com/questions/77287622/modulenotfounderror-no-module-named-kafka-vendor-six-moves-in-dockerized-djan
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from data_generator import generate_fake_user

today = datetime.datetime.now()
SECONDS = 1


def stream_data():

    producer = KafkaProducer(bootstrap_servers="broker:9092", max_block_ms=10_000*SECONDS)
    print("--"*20)
    print("Sending data ... ")
    print("--"*20)
    for _ in range(100):
        user = generate_fake_user()
        data = json.dumps(user, default=str).encode("utf-8")
        producer.send("user_data", value=data)

@dag(dag_id="stream_data", start_date=datetime.datetime(2021, 1, 1), schedule_interval="@daily")
def service_dag():
    PythonOperator(
        task_id="streaming_task",
        python_callable=stream_data
    )

service_dag()

# import datetime

# from airflow.decorators import dag
# from airflow.operators.empty import EmptyOperator


# @dag(dag_id="dag_id2", start_date=datetime.datetime(2021, 1, 1), schedule="@daily")
# def generate_dag2():
#     EmptyOperator(task_id="task2")


# generate_dag2()