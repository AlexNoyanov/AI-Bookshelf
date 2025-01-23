import pymysql
from config.config import DB_CONFIG

class Database:
    def __init__(self):
        self.config = DB_CONFIG

    def connect(self):
        return pymysql.connect(**self.config)

    def execute_query(self, query, params=None):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return cursor

    def fetch_one(self, query, params=None):
        with self.connect() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()

    def fetch_all(self, query, params=None):
        with self.connect() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
