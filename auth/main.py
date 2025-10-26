import os.path
import sqlite3

from auth.models import *
from typing import Any, Optional

class Database:
    def __init__(self):
        self.__con = sqlite3.connect("emberhacks.db")
        self.__cur = self.__con.cursor()
        self.__init_db()

    @staticmethod
    def __read_sql_file(file_path: str) -> str:
        """Reads SQL from a file, verifying that file exists.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"SQL initialization file not found: {file_path}")

        sql_request: str = ""
        with open(file_path, "r", encoding="utf-8") as f:
            # Read the whole file to capture multiline SQL statements
            sql_request = f.read()
        return sql_request.strip()

    def __exec(self, sql: str, data: tuple) -> None:
        try:
            self.__cur.execute(sql, data)
            self.__con.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to post user: {e}")
            self.__con.rollback()
            raise

    def __init_db(self):
        """
        Initializes the database structure by executing SQL files.
        Relies on 'resources/db_init_users.sql' and 'resources/db_init_requests.sql' existing.
        """
        print("[INFO] Started initialization")
        files = ["users", "requests"]
        try:
            for file in files:
                sql_request = self.__read_sql_file(
                    f"resources/db_init_{file}.sql")
                self.__con.execute(sql_request)

            # CRITICAL: Commit the creation of tables to the disk
            self.__con.commit()
            print("[INFO] DB init complete")

        except Exception as e:
            print(f"[ERROR] DB initialization failed: {e}")
            self.__con.rollback()
            raise

    def post_user(self, user_dto: UserDto) -> User:
        sql = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        data = (user_dto.username, user_dto.email, user_dto.password)
        print("[INFO] POST users")
        self.__exec(sql, data)
        user = User.from_dto(user_dto)
        user.id = self.__cur.lastrowid
        print("[Res")
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        sql = "SELECT id, username, email, password FROM users WHERE id = ?"
        self.__exec(sql, (user_id,))

        record = self.__cur.fetchone()

        if record is None:
            return None
        return User.from_record(record)

    def post_request(self, dto: RequestDto) -> RequestDtoResponse:
        if dto.author_id is None or self.get_user(dto.author_id):
            raise
        sql = ("INSERT INTO requests (author_id, req, response, created)"
               " VALUES (?, ?, ?, ?)")
        request = Request.from_dto(dto)
        data = (request.author_id, request.req, request.response,
                request.timestamp)
        self.__exec(sql, data)
        request.id = self.__cur.lastrowid
        return request.to_dto()

    def get_all_requests_by_user_id(self, user_id: int) -> list[RequestDto]:
        if self.get_user(user_id) is None:
            raise

        sql = "SELECT * FROM requests WHERE author_id = ?"
        self.__exec(sql, (user_id, ))
        return [Request.from_record(record).to_dto()
                for record in self.__cur.fetchall()]

    def __del__(self):
        try:
            if hasattr(self, '_Database__con') and self.__con:
                self.__con.close()
                print("[INFO] Database connection successfully closed.")
        except Exception:
            pass
