import sqlite3 as sql


class DataBase:
    def __init__(self):
        self.con = sql.connect("users.db")
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE users (
                                        id       INTEGER PRIMARY KEY
                                                         UNIQUE
                                                         NOT NULL,
                                        login    TEXT    NOT NULL,
                                        password TEXT    NOT NULL
                                    );
                                    """)
        self.con.commit()

    def add_user(self, login: str, password: str):
        ...

    def authorization(self, login: str, password: str):
        ...
