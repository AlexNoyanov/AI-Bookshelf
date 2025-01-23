from utils.db import Database

class User:
    def __init__(self):
        self.db = Database()

    def create_user(self, user_id, username):
        query = """
        INSERT IGNORE INTO users (user_id, username)
        VALUES (%s, %s)
        """
        self.db.execute_query(query, (user_id, username))

    def get_user(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        return self.db.fetch_one(query, (user_id,))
