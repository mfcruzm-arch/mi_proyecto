"""Crea y comprueba generos de ejemplo en la base de datos."""

import sqlite3
from pathlib import Path

from libro import Genero


RUTA_BASE_DATOS = Path(__file__).resolve().parent / "biblioteca.db"


def crear_generos() -> list[Genero]:
    """Inserta generos de ejemplo y devuelve los registros guardados."""
    generos = [Genero(None, "comedia"), Genero(None, "terror"), Genero(None, "accion")]

    with sqlite3.connect(RUTA_BASE_DATOS) as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS generos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
            """
        )
        conexion.executemany(
            "INSERT OR IGNORE INTO generos (nombre) VALUES (?)",
            [(genero.nombre,) for genero in generos],
        )
        filas = conexion.execute(
            """
            SELECT id, nombre FROM generos
            WHERE nombre IN ('comedia', 'terror', 'accion')
            ORDER BY id
            """
        ).fetchall()

    return [Genero(id, nombre) for id, nombre in filas]


if __name__ == "__main__":
    for genero in crear_generos():
        print(genero)
