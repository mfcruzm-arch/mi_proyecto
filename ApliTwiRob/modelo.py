"""Modelo de datos de ApliTwiRob.

Este modulo contiene SQLite y las reglas de usuarios y tweets. No conoce
nada de Tkinter ni de la interfaz grafica.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "twitter.db"
MAX_TWEET_LENGTH = 280


class TwitterError(Exception):
    """Error controlado de la aplicacion."""


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Abre, confirma y cierra una conexion SQLite de forma segura."""
    DATA_DIR.mkdir(exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()


def create_db() -> None:
    """Crea las tablas de la aplicacion si no existen."""
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                bio TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS tweet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                user_id INTEGER NOT NULL REFERENCES user(id) ON DELETE CASCADE,
                retweet_from INTEGER REFERENCES tweet(id) ON DELETE CASCADE
            );
            """
        )


class User:
    """Entidad de usuario y operaciones de dominio relacionadas."""

    def __init__(
        self,
        username: str,
        password: str = "",
        bio: str = "",
        user_id: int = 0,
    ) -> None:
        self.username = username
        self.password = password
        self.bio = bio
        self.id = user_id
        self.logged = False

    def save(self) -> None:
        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO user (username, password, bio) VALUES (?, ?, ?)",
                (self.username, self.password, self.bio),
            )
            self.id = cursor.lastrowid or 0

    def update(self) -> None:
        """Actualiza los datos de un usuario existente."""
        if not self.id:
            raise TwitterError("El usuario no tiene un identificador valido.")
        with get_connection() as connection:
            connection.execute(
                "UPDATE user SET username = ?, password = ?, bio = ? WHERE id = ?",
                (self.username, self.password, self.bio, self.id),
            )

    def login(self, password: str) -> bool:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT id, username, bio FROM user "
                "WHERE username = ? AND password = ?",
                (self.username, password),
            ).fetchone()
        if row is None:
            return False
        self.id = row["id"]
        self.bio = row["bio"]
        self.logged = True
        return True

    def change_password(self, new_password: str) -> None:
        with get_connection() as connection:
            connection.execute(
                "UPDATE user SET password = ? WHERE id = ?",
                (new_password, self.id),
            )
        self.password = new_password

    def delete_account(self) -> None:
        with get_connection() as connection:
            connection.execute("DELETE FROM user WHERE id = ?", (self.id,))
        self.logged = False

    def publish_tweet(self, content: str) -> None:
        if not self.logged:
            raise TwitterError("Debes iniciar sesion.")
        content = content.strip()
        if not content:
            raise TwitterError("El tweet no puede estar vacio.")
        if len(content) > MAX_TWEET_LENGTH:
            raise TwitterError(f"El tweet no puede superar {MAX_TWEET_LENGTH} caracteres.")
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO tweet (content, user_id) VALUES (?, ?)",
                (content, self.id),
            )

    def retweet(self, tweet_id: int) -> None:
        if not self.logged:
            raise TwitterError("Debes iniciar sesion.")
        with get_connection() as connection:
            exists = connection.execute(
                "SELECT 1 FROM tweet WHERE id = ?", (tweet_id,)
            ).fetchone()
            if exists is None:
                raise TwitterError("El tweet no existe.")
            connection.execute(
                "INSERT INTO tweet (content, user_id, retweet_from) VALUES (?, ?, ?)",
                ("", self.id, tweet_id),
            )


def get_timeline() -> list[str]:
    """Devuelve el timeline listo para ser mostrado por la vista."""
    timeline: list[str] = []
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT t.id, t.content, t.retweet_from, u.username "
            "FROM tweet AS t JOIN user AS u ON t.user_id = u.id "
            "ORDER BY t.id DESC"
        ).fetchall()
        for row in rows:
            content = row["content"]
            prefix = "[RT] " if row["retweet_from"] else ""
            if row["retweet_from"]:
                original = connection.execute(
                    "SELECT content FROM tweet WHERE id = ?",
                    (row["retweet_from"],),
                ).fetchone()
                content = original["content"] if original else "[Tweet eliminado]"
            timeline.append(f"[{row['id']}] @{row['username']}: {prefix}{content}")
    return timeline


def delete_tweet(tweet_id: int, user_id: int) -> bool:
    """Elimina un tweet si pertenece al usuario indicado."""
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tweet WHERE id = ? AND user_id = ?",
            (tweet_id, user_id),
        )
        return cursor.rowcount > 0


def get_users() -> list[User]:
    """Devuelve los usuarios completos ordenados por nombre."""
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, username, password, bio FROM user "
            "ORDER BY username COLLATE NOCASE"
        ).fetchall()
    return [
        User(row["username"], row["password"], row["bio"] or "", row["id"])
        for row in rows
    ]


def delete_users(user_ids: list[int]) -> list[str]:
    """Elimina varios usuarios y devuelve los nombres que fueron eliminados."""
    unique_ids = list(dict.fromkeys(user_ids))
    if not unique_ids:
        return []
    placeholders = ", ".join("?" for _ in unique_ids)
    with get_connection() as connection:
        rows = connection.execute(
            f"SELECT username FROM user WHERE id IN ({placeholders}) ORDER BY username COLLATE NOCASE",
            unique_ids,
        ).fetchall()
        connection.execute(
            f"DELETE FROM user WHERE id IN ({placeholders})",
            unique_ids,
        )
    return [row["username"] for row in rows]