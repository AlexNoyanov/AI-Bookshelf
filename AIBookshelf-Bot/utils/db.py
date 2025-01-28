import mysql.connector
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'your_database')
            )
            self.cur = self.conn.cursor(dictionary=True)
            logger.info("Database connection established successfully")
        except mysql.connector.Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            self.conn = None
            self.cur = None
            raise

    def log_user_activity(self, user_id: int, username: str, action_type: str, message: str = None):
        """Log user activity to user_logs table"""
        if not self.conn or not self.cur:
            logger.error("No database connection available")
            return
            
        try:
            sql = """
            INSERT INTO user_logs (
                user_id, username, action_type, message_text
            ) VALUES (%s, %s, %s, %s)
            """
            self.cur.execute(sql, (user_id, username, action_type, message))
            self.conn.commit()
            logger.debug(f"Logged activity for user {user_id}: {action_type}")
        except Exception as e:
            logger.error(f"Error logging user activity: {e}")
            self.conn.rollback()

    def insert_user(self, user_id: int, username: str):
        if not self.conn or not self.cur:
            logger.error("No database connection available")
            return
            
        try:
            self.cur.execute(
                "INSERT IGNORE INTO users (user_id, username) VALUES (%s, %s)",
                (user_id, username)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error inserting user: {e}")
            self.conn.rollback()

    def insert_book(self, user_id: int, book_name: str, file_id: str, file_size: int):
        if not self.conn or not self.cur:
            logger.error("No database connection available")
            return None
            
        try:
            self.cur.execute(
                """
                INSERT INTO books (user_id, book_name, file_id, file_size) 
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, book_name, file_id, file_size)
            )
            self.conn.commit()
            return self.cur.lastrowid
        except Exception as e:
            logger.error(f"Error inserting book: {e}")
            self.conn.rollback()
            return None

    def get_user_books(self, user_id: int):
        if not self.conn or not self.cur:
            logger.error("No database connection available")
            return []
            
        try:
            self.cur.execute(
                "SELECT * FROM books WHERE user_id = %s ORDER BY uploaded_at DESC",
                (user_id,)
            )
            return self.cur.fetchall()
        except Exception as e:
            logger.error(f"Error getting user books: {e}")
            return []

    def close(self):
        try:
            if hasattr(self, 'cur') and self.cur:
                self.cur.close()
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

    def __del__(self):
        self.close()
