from utils.db import Database

class Book:
    def __init__(self):
        self.db = Database()

    def add_book(self, user_id, book_name, file_id, file_size):
        query = """
        INSERT INTO books (user_id, book_name, file_id, file_size)
        VALUES (%s, %s, %s, %s)
        """
        self.db.execute_query(query, (user_id, book_name, file_id, file_size))

    def get_user_books(self, user_id):
        query = """
        SELECT * FROM v_books_with_metadata 
        WHERE user_id = %s AND is_deleted = FALSE
        """
        return self.db.fetch_all(query, (user_id,))

    def delete_book(self, book_id, user_id):
        query = """
        UPDATE books SET is_deleted = TRUE 
        WHERE id = %s AND user_id = %s
        """
        self.db.execute_query(query, (book_id, user_id))
