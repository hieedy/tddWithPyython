import os
import sqlite3
import uuid
from typing import List
from pydantic import BaseModel, EmailStr, Field


class NotFound(Exception):
    pass


class DB:

    def __init__(self):
        self.con = sqlite3.connect(os.getenv('DATABASE_NAME','database.db'))

    def get_con(self):
        return self.con

def get_connection():
    return sqlite3.connect(os.getenv('DATABASE_NAME','database.db'))

class Article(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author: EmailStr
    title: str
    content: str

    @classmethod
    def get_by_id(cls, article_id: str):
        con = get_connection()
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute('Select * from articles where id = ?', (article_id,))

        record = cur.fetchone()

        if record is None:
            raise NotFound

        article = cls(**record)
        con.close()

        return article

    @classmethod
    def get_by_title(cls, title: str):
        con = get_connection()
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute('Select * FROM articles WHERE title = ?',(title,))

        record = cur.fetchone()
        if record is None:
            raise NotFound

        article = cls(**record)
        con.close()
        return article

    @classmethod
    def list(cls) -> List["Article"]:
        con = get_connection()
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("Select * FROM articles")

        records = cur.fetchall()
        articles = [cls(**record) for record in records]
        con.close()

        return articles

    def save(self) -> "Article":
        with get_connection() as con:
            cur = con.cursor()
            cur.execute(
                        "INSERT into articles(id,author,title,content) VALUES(?,?,?,?)",
                        (self.id, self.author, self.title, self.content)
            )
            con.commit()

        return self

    @classmethod
    def create_table(cls,database_name='database.db'):
        con = sqlite3.connect(database_name)
        con.execute(
            "CREATE TABLE IF NOT EXISTS articles(id TEXT, author TEXT, title TEXT, content TEXT)"
        )
        con.close()


