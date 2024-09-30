import sys
import logging
from typing import TypeVar, Optional, Callable
from functools import wraps

from cassandra.cluster import Cluster, Session as CassandraSession

from pyspark.sql import SparkSession, Row, DataFrame

from data.user import User
from data.db import CassandraUsersDB


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("spark_writer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

T = TypeVar("T")


def catch(func: Callable[..., T]) -> Callable[..., Optional[T]]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Optional[T]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error in {func.__name__} due to {e}")
            return None

    return wrapper


@catch
def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder.master("local")  # type: ignore
        .appName("SparkDataStreaming")
        .config("spark.cassandra.connection.host", "localhost")
        .config(
            "spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2"
        )
        .getOrCreate()
    )


@catch
def create_cassandra_connection() -> CassandraSession:
    return Cluster(["localhost"]).connect()


@catch
def create_kafka_connection(spark_conn: SparkSession) -> DataFrame:
    return (
        spark_conn.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "user_data")
        .load()
    )


def insert_user(row: Row):
    sess = create_cassandra_connection()
    if sess is None:
        logging.error("Could not create cassandra connection")
        return

    users_db = CassandraUsersDB(sess)
    user = User.from_json(row.value)
    print(user)
    users_db.insert_user(user)

    logging.info(f"Inserted user {row.value}")


def create_stream_writer(kafka_conn: DataFrame):
    return (
        kafka_conn.selectExpr("CAST(value AS STRING)")
        .writeStream.format("console")
        .foreach(insert_user)
        .start()
    )


def main():
    # Create the cassandra connection
    cassandra_sess = create_cassandra_connection()
    if cassandra_sess is None:
        logging.error("Could not create cassandra connection")
        sys.exit(1)
    logging.info("Cassandra connection created successfully")

    users_db = CassandraUsersDB(cassandra_sess)
    users_db.create_keyspace()
    users_db.create_users_table()

    # Create the spark session
    spark_sess = create_spark_session()
    if spark_sess is None:
        logging.error("Could not create spark session")
        sys.exit(1)
    logging.info("Spark session created successfully")

    # Create the kafka connection
    df = create_kafka_connection(spark_sess)
    if df is None:
        logging.error("Could not create kafka connection")
        sys.exit(1)
    logging.info("Kafka connection created successfully")

    # Create the stream writer
    stream = create_stream_writer(df)
    stream.awaitTermination()

    logging.info("Cassandra connection created successfully")
    cassandra_sess.shutdown()

if __name__ == "__main__":
    main()

    # from dags.data_generator import generate_fake_user
    # user = generate_fake_user()
    # insert_user(Row(value=json.dumps(user.json())))