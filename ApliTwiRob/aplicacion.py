"""Controlador de ApliTwiRob.

Coordina la vista y el modelo. Este modulo no crea ventanas ni muestra
mensajes: eso pertenece a ``chat.py``.
"""

from __future__ import annotations

import sqlite3

from modelo import TwitterError, User, delete_tweet, delete_users, get_timeline, get_users


class TwitterApplication:
    """Casos de uso disponibles para la vista de chat."""

    def __init__(self) -> None:
        self.current_user: User | None = None

    @property
    def is_logged_in(self) -> bool:
        return self.current_user is not None

    def login(self, username: str, password: str) -> User:
        if not username or not password:
            raise TwitterError("Introduce usuario y contrasena.")
        user = User(username)
        if not user.login(password):
            raise TwitterError("Las credenciales no son correctas.")
        self.current_user = user
        return user

    def register(self, username: str, password: str, bio: str = "") -> None:
        if not username or not password:
            raise TwitterError("El usuario y la contrasena son obligatorios.")
        try:
            User(username, password, bio).save()
        except sqlite3.IntegrityError as error:
            raise TwitterError("Ese nombre de usuario ya existe.") from error

    def logout(self) -> None:
        self.current_user = None

    def change_password(self, new_password: str) -> None:
        user = self._require_user()
        if not new_password.strip():
            raise TwitterError("La contrasena no puede estar vacia.")
        user.change_password(new_password.strip())

    def delete_account(self) -> None:
        user = self._require_user()
        user.delete_account()
        self.logout()

    def publish(self, content: str) -> None:
        self._require_user().publish_tweet(content)

    def retweet(self, tweet_id: int) -> None:
        self._require_user().retweet(tweet_id)

    def timeline(self) -> list[str]:
        return get_timeline()

    def users(self) -> list[User]:
        return get_users()

    def update_user(self, user_id: int, username: str, password: str, bio: str) -> None:
        if not username or not password:
            raise TwitterError("El nombre y la contrasena son obligatorios.")
        user = User(username, password, bio, user_id)
        try:
            user.update()
        except sqlite3.IntegrityError as error:
            raise TwitterError("Ese nombre de usuario ya existe.") from error
        if self.current_user and self.current_user.id == user_id:
            self.current_user.username = username
            self.current_user.password = password
            self.current_user.bio = bio

    def remove_users(self, user_ids: list[int]) -> list[str]:
        if not user_ids:
            raise TwitterError("Selecciona al menos un usuario.")
        deleted_usernames = delete_users(user_ids)
        if not deleted_usernames:
            raise TwitterError("No se encontraron los usuarios seleccionados.")
        if self.current_user and self.current_user.id in user_ids:
            self.logout()
        return deleted_usernames

    def remove_tweet(self, tweet_id: int) -> None:
        user = self._require_user()
        if not delete_tweet(tweet_id, user.id):
            raise TwitterError("El tweet no existe o no pertenece a tu cuenta.")

    def _require_user(self) -> User:
        if self.current_user is None:
            raise TwitterError("Inicia sesion primero.")
        return self.current_user