import psycopg
import pathlib

from psycopg.sql import SQL
from database.utils import Message

class MessagesDB:
    path_prefix = pathlib.Path("database/sql/messages")

    def __init__(self, url: str):
        self.url = url
        self.create_table()

    def __enter__(self):
        self._conn = psycopg.connect(self.url)
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._conn.close()


    def _read(self, path: str):
        path = self.path_prefix / path

        with open(path, "r") as file:
            data = file.read()
            file.close()

        sql = SQL(data)
        return sql


    def fetch_all(self, sql: SQL):
        with self as conn:
            return conn.execute(sql).fetchall()


    def create_table(self):
        with self as conn:
            sql = self._read("create.sql")
            conn.execute(sql)


    def add_message(self, message: Message):
        with self as conn:
            sql = self._read("insert.sql")
            conn.execute(sql, params=message.to_list())


    def get_all_messages(self):
        sql = self._read("select.sql")
        rows = self.fetch_all(sql)

        return [{"author": author, "text": text} for [author, text] in rows]