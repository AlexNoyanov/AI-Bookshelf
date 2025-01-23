# import pymysql
# from config.config import DB_CONFIG

# class Database:
#     def __init__(self):
#         self.config = DB_CONFIG

#     def connect(self):
#         return pymysql.connect(**self.config)

#     def execute_query(self, query, params=None):
#         with self.connect() as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query, params)
#                 connection.commit()
#                 return cursor

#     def fetch_one(self, query, params=None):
#         with self.connect() as connection:
#             with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#                 cursor.execute(query, params)
#                 return cursor.fetchone()

#     def fetch_all(self, query, params=None):
#         with self.connect() as connection:
#             with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#                 cursor.execute(query, params)
#                 return cursor.fetchall()

# utils/db.py
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }

    def test_connection(self):
        try:
            with self.connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    print("Database connection successful!")
                    return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    def connect(self):
        return pymysql.connect(**self.config)
