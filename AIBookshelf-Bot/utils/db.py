import mysql.connector
from datetime import datetime
from typing import Optional, List, Dict
import os
from dotenv import load_dotenv
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Validate required environment variables
        required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.debug("Loading database configuration...")
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'connect_timeout': 10
        }
        
        # Log configuration (without password)
        safe_config = self.config.copy()
        safe_config['password'] = '***'
        logger.debug(f"Database configuration: {safe_config}")

    def get_connection(self):
        try:
            logger.debug("Attempting to establish database connection...")
            connection = mysql.connector.connect(**self.config)
            logger.debug("Database connection established successfully")
            return connection
        except mysql.connector.Error as e:
            logger.error(f"Database connection error: {e}", exc_info=True)
            raise

    def get_user_books(self, user_id: int) -> List[Dict]:
        """Get all books for a user with metadata"""
        query = """
        SELECT b.*, bm.title, bm.author, bm.page_count, 
               GROUP_CONCAT(c.name) as categories
        FROM books b
        LEFT JOIN book_metadata bm ON b.id = bm.book_id
        LEFT JOIN book_categories bc ON b.id = bc.book_id
        LEFT JOIN categories c ON bc.category_id = c.id
        WHERE b.user_id = %s AND b.is_deleted = FALSE
        GROUP BY b.id
        ORDER BY b.uploaded_at DESC
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (user_id,))
                    books = cursor.fetchall()
                    logger.debug(f"Retrieved {len(books)} books for user {user_id}")
                    return books
        except Exception as e:
            logger.error(f"Error getting books for user {user_id}: {e}")
            return []

    def insert_user(self, user_id: int, username: str) -> None:
        """Insert or update user in the database"""
        query = """
        INSERT INTO users (user_id, username, last_active_at) 
        VALUES (%s, %s, NOW()) 
        ON DUPLICATE KEY UPDATE 
            username = VALUES(username),
            last_active_at = NOW()
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, username))
            conn.commit()

    def insert_book(self, user_id: int, book_name: str, file_id: str, 
                   file_size: int) -> Optional[int]:
        """Insert a new book record"""
        query = """
        INSERT INTO books (user_id, book_name, file_id, file_size, uploaded_at) 
        VALUES (%s, %s, %s, %s, NOW())
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, book_name, file_id, file_size))
                book_id = cursor.lastrowid
            conn.commit()
            return book_id

    def update_book_metadata(self, book_id: int, metadata: Dict) -> None:
        """Update book metadata"""
        query = """
        INSERT INTO book_metadata (
            book_id, title, author, publication_year, 
            page_count, language, description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            author = VALUES(author),
            publication_year = VALUES(publication_year),
            page_count = VALUES(page_count),
            language = VALUES(language),
            description = VALUES(description)
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    book_id,
                    metadata.get('title'),
                    metadata.get('author'),
                    metadata.get('publication_year'),
                    metadata.get('page_count'),
                    metadata.get('language'),
                    metadata.get('description')
                ))
            conn.commit()

    def add_book_category(self, book_id: int, category_name: str) -> None:
        """Add a category to a book, creating the category if it doesn't exist"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # First, get or create category
                cursor.execute(
                    "INSERT IGNORE INTO categories (name) VALUES (%s)",
                    (category_name,)
                )
                conn.commit()
                
                # Get category id
                cursor.execute(
                    "SELECT id FROM categories WHERE name = %s",
                    (category_name,)
                )
                category_id = cursor.fetchone()[0]
                
                # Add book-category relationship
                cursor.execute("""
                    INSERT IGNORE INTO book_categories (book_id, category_id)
                    VALUES (%s, %s)
                """, (book_id, category_id))
                conn.commit()

    def get_book(self, book_id: int) -> Optional[Dict]:
        """Get a single book with all its metadata"""
        query = """
        SELECT b.*, bm.*, GROUP_CONCAT(c.name) as categories
        FROM books b
        LEFT JOIN book_metadata bm ON b.id = bm.book_id
        LEFT JOIN book_categories bc ON b.id = bc.book_id
        LEFT JOIN categories c ON bc.category_id = c.id
        WHERE b.id = %s AND b.is_deleted = FALSE
        GROUP BY b.id
        """
        with self.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (book_id,))
                return cursor.fetchone()
