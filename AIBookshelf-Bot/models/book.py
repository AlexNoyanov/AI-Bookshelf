from utils.db import Database

class Book:
    def __init__(self):
        self.db = Database()

    def add_book(self, user_id, book_name, file_id, file_size):
        query = """
        INSERT INTO books (user_id, book_name, file_id, file_size)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        return self.db.execute_query(query, (user_id, book_name, file_id, file_size))

    def get_user_books(self, user_id):
        query = """
        SELECT b.*, bm.title, bm.author 
        FROM books b
        LEFT JOIN book_metadata bm ON b.id = bm.book_id
        WHERE b.user_id = %s AND b.is_deleted = FALSE
        ORDER BY b.uploaded_at DESC
        """
        return self.db.fetch_all(query, (user_id,))

    def get_book(self, book_id, user_id):
        query = """
        SELECT * FROM books 
        WHERE id = %s AND user_id = %s AND is_deleted = FALSE
        """
        return self.db.fetch_one(query, (book_id, user_id))

    def delete_book(self, book_id, user_id):
        query = """
        UPDATE books 
        SET is_deleted = TRUE 
        WHERE id = %s AND user_id = %s AND is_deleted = FALSE
        """
        result = self.db.execute_query(query, (book_id, user_id))
        return result.rowcount > 0
