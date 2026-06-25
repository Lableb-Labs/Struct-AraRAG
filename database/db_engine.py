# db_engine.py

import psycopg2
from database.config import DB_CONFIG


class PostgresDB:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        """
        Execute SELECT queries safely
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute_command(self, query, params=None):
        """
        Execute INSERT / UPDATE / DELETE
        """
        self.cursor.execute(query, params)

    def close(self):
        self.cursor.close()
        self.conn.close()