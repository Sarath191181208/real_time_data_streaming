import logging
import uuid
from data.user import User
from cassandra.cluster import Session as CassandraSession


class CassandraUsersDB:
    KEYSPACE = "spark_streams"
    TABLE = "created_users"

    def __init__(self, session: CassandraSession) -> None:
        self.session = session

    def create_keyspace(self) -> None:
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.KEYSPACE}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}};
        """)

        logging.info(f"{'##'*20}Keyspace created successfully {'##'*20}")

    def create_users_table(self) -> None:
        self.session.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.KEYSPACE}.{self.TABLE}(
            id UUID PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            city TEXT,
            post_code TEXT,
            email TEXT,
            username TEXT,
            registered_date TEXT,
            phone TEXT,
            picture TEXT);
        """)

        logging.info(f"{'##'*20}Table created successfully {'##'*20}")

    def insert_user(self, user: User) -> None:
        id = uuid.uuid4()
        self.session.execute(
            f"""
        INSERT INTO {self.KEYSPACE}.{self.TABLE}(
            id,
            first_name,
            last_name,

            gender, 
            city, 
            post_code,

            email,
            username,
            registered_date,

            phone,
            picture)
        VALUES( 
            %s, %s, %s, 
            %s, %s, %s,
            %s, %s, %s, 
            %s, %s
        )""",
            (
                id,
                user.name.first,
                user.name.last,

                user.gender,
                user.location.city,
                user.location.postcode,

                user.email,
                user.login.username,
                user.registered.date,

                user.phone,
                user.picture.thumbnail,
            ),
        )
