from __future__ import annotations

import re
import sqlite3

DEBUGGING = False  # Controla el mostrado de las trazas para depuración
DB_PATH = 'twitter.db'

RETWEET_PREFIX = '[RT]'
MAX_TWEET_LENGTH = 280


def conexion_db(db_path):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur


def create_db(db_path: str = DB_PATH) -> None:
    """Crea la base de datos en la ruta db_path y las tablas."""
    con, cur = conexion_db(db_path)
    sql = """
        DROP TABLE IF EXISTS tweet;
        DROP TABLE IF EXISTS user;
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            bio TEXT
        );
        CREATE TABLE IF NOT EXISTS tweet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL REFERENCES user (id),
            retweet_from INTEGER REFERENCES tweet (id)
        );
    """
    cur.executescript(sql)
    con.commit()
    con.close()


class User:
    con, cur = conexion_db(DB_PATH)

    def __init__(self, username: str, password: str, bio: str = '', user_id: int = 0):
        self.con = self.__class__.con
        self.cur = self.__class__.cur
        self.username = username
        self.password = password
        self.bio = bio
        self.id = user_id
        self.logged = False

    def __del__(self):
        try:
            if hasattr(self, 'con') and self.con is not None:
                self.con.close()
        except Exception:
            pass

    def save(self) -> None:
        sql = "INSERT INTO user (username, password, bio) VALUES (?, ?, ?)"
        self.cur.execute(sql, (self.username, self.password, self.bio))
        self.id = self.cur.lastrowid
        self.con.commit()

    def login(self, password: str) -> None:
        sql = """
            SELECT COUNT(*) AS logged
            FROM user
            WHERE id = ? AND password = ?
        """
        row = self.cur.execute(sql, (self.id, password)).fetchone()
        self.logged = bool(row['logged']) if row is not None else False

    def tweet(self, content: str) -> 'Tweet':
        if not self.logged:
            raise TwitterError(f'User {self.username} is not logged in!')
        if len(content) > MAX_TWEET_LENGTH:
            raise TwitterError('Tweet has more than 280 chars!')

        tweet = Tweet(content=content)
        tweet.save(self)
        return tweet

    def retweet(self, tweet_id: int) -> 'Tweet':
        if not self.logged:
            raise TwitterError(f'User {self.username} is not logged in!')

        sql = "SELECT id FROM tweet WHERE id = ?"
        row = self.cur.execute(sql, (tweet_id,)).fetchone()
        if row is None:
            raise TwitterError(f'Tweet with id {tweet_id} does not exist!')

        tweet = Tweet(retweet_from=tweet_id)
        tweet.save(self)
        return tweet

    @property
    def tweets(self):
        sql = "SELECT * FROM tweet WHERE user_id = ? ORDER BY id"
        rows = self.cur.execute(sql, (self.id,)).fetchall()
        for row in rows:
            yield Tweet.from_db_row(row)

    def __repr__(self):
        return f'{self.username}: {self.bio}'

    __str__ = __repr__

    @classmethod
    def from_db_row(cls, row: sqlite3.Row) -> 'User':
        return cls(
            row['username'],
            row['password'],
            row['bio'],
            row['id'],
        )


class Tweet:
    con, cur = conexion_db(DB_PATH)

    def __init__(self, content: str = '', retweet_from: int = 0, tweet_id: int = 0):
        self.con = self.__class__.con
        self.cur = self.__class__.cur
        self.retweet_from = retweet_from
        self.id = tweet_id
        self._content = '' if retweet_from else content

    def __del__(self):
        try:
            if hasattr(self, 'con') and self.con is not None:
                self.con.close()
        except Exception:
            pass

    @property
    def is_retweet(self) -> bool:
        return bool(self.retweet_from)

    @property
    def content(self) -> str:
        if not self.is_retweet:
            return self._content

        sql = "SELECT content FROM tweet WHERE id = ?"
        row = self.cur.execute(sql, (self.retweet_from,)).fetchone()
        if row is None:
            return ''
        return row['content']

    def save(self, user: User) -> None:
        sql = "INSERT INTO tweet (content, user_id, retweet_from) VALUES (?, ?, ?)"
        self.cur.execute(sql, (self._content, user.id, self.retweet_from))
        self.id = self.cur.lastrowid
        self.con.commit()

    def __repr__(self):
        prefix = f'{RETWEET_PREFIX} ' if self.is_retweet else ''
        return f'{prefix}{self.content} (id={self.id})'

    __str__ = __repr__

    @classmethod
    def from_db_row(cls, row: sqlite3.Row) -> 'Tweet':
        return cls(
            content=row['content'],
            retweet_from=row['retweet_from'] or 0,
            tweet_id=row['id'],
        )


class Twitter:
    con, cur = conexion_db(DB_PATH)

    def __init__(self):
        self.con = self.__class__.con
        self.cur = self.__class__.cur

    def add_user(self, username: str, password: str, bio: str = '') -> User:
        if not self._valid_password(password):
            raise TwitterError('Password does not follow security rules!')

        user = User(username, password, bio)
        user.save()
        return user

    @staticmethod
    def _valid_password(password: str) -> bool:
        pattern = r'^(?=[=@])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[=@][A-Za-z0-9!@#$%^&*]{5,10}$'
        return bool(re.fullmatch(pattern, password))

    def get_user(self, user_id: int) -> User:
        sql = "SELECT * FROM user WHERE id = ?"
        row = self.cur.execute(sql, (user_id,)).fetchone()
        if row is None:
            raise TwitterError(f'User with id {user_id} does not exist!')
        return User.from_db_row(row)


class TwitterError(Exception):
    def __init__(self, message):
        super().__init__(message)


if __name__ == '__main__':
    create_db(DB_PATH)
    usuario1 = User('Roberto Herrera', '1234', 'Esta es la bio.')
    print(usuario1)
    usuario1.save()
    usuario1.login('')
    try:
        usuario1.tweet('Qué ilusión me hace twitear!')
    except TwitterError:
        print('Se ha producido una excepción.')
    usuario1.login('1234')
    try:
        usuario1.tweet('Qué Alegria poder hace twitear!')
    except TwitterError:
        print('Se ha producido una excepción.')
    try:
        usuario1.retweet(1000)
    except TwitterError:
        print('Se ha producido una excepción al re-twitear.')
