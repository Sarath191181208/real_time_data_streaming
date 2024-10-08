import datetime
import json
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from kafka import KafkaProducer

import logging
import six
import sys

# https://stackoverflow.com/questions/77287622/modulenotfounderror-no-module-named-kafka-vendor-six-moves-in-dockerized-djan
if sys.version_info >= (3, 12, 0):
    sys.modules["kafka.vendor.six.moves"] = six.moves

from data_generator import generate_fake_user


logging.basicConfig(
    filename="log.log",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


today = datetime.datetime.now()
SECONDS = 1


def stream_data():
    try:
        producer = KafkaProducer(bootstrap_servers="broker:29092")
        logging.info("Connected to kafka")
        logging.info("--" * 20)
        logging.info("Sending data ... ")
        logging.info("--" * 20)
        for i in range(10):
            user = generate_fake_user()
            data = json.dumps(user.json()).encode("utf-8")
            logging.info(f"Sending the user data {i}")
            logging.info(data)
            producer.send("user_data", value=data)
        producer.flush()
        logging.info(f"{'##'*20}Sending completed{'##'*20}")
    except Exception:
        logging.exception("Writing to kafka failed with the following error")


@dag(
    dag_id="stream_data",
    start_date=datetime.datetime(2021, 1, 1),
    schedule_interval="@daily",
)
def service_dag():
    PythonOperator(task_id="streaming_task", python_callable=stream_data)


service_dag()
