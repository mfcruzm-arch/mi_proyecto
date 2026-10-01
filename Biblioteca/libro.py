"""Modelos y operaciones CRUD para libros y generos."""

import sqlite3
from pathlib import Path
from typing import Any, ClassVar


class Libro:
    def __init__(
        self,
        id,
        titulo,
        autor,
        genero_id,
        anio,
        paginas,
        valoracion=0.0,
        estado="Pendiente",
        favorito=0,
        notas=None,
    ):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero_id = genero_id
        self.anio = anio
        self.paginas = paginas
        self.valoracion = valoracion
        self.estado = estado
        self.favorito = favorito
        self.notas = notas

    def __repr__(self):
        return f"<Libro {self.id}: '{self.titulo}' - {self.autor}>"

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class Genero:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def __repr__(self):
        return f"<Genero {self.id}: {self.nombre}>"


class LibroCRUD:
    """Gestiona la creacion, consulta, modificacion y eliminacion de libros."""

    _db_path: Path = Path(__file__).resolve().parent / "biblioteca.db"
    _connection: sqlite3.Connection | None = None
    _campos_actualizables: ClassVar[frozenset[str]] = frozenset({
        "titulo",
        "autor",
        "genero_id",
        "anio",
        "paginas",
        "valoracion",
        "estado",
        "favorito",
        "notas",
    })

    @classmethod
    def conectar(cls, db_path: str | None = None) -> None:
        """Inicializa o cambia la conexion compartida."""
        if db_path:
            cls._db_path = Path(db_path)

        cls.cerrar_conexion()
        cls._connection = sqlite3.connect(database=cls._db_path)
        cls._connection.row_factory = sqlite3.Row
        cls._connection.execute("PRAGMA foreign_keys = ON")

    @classmethod
    def obtener_conexion(cls) -> sqlite3.Connection:
        """Devuelve la conexion activa y la crea si es necesario."""
        if cls._connection is None:
            cls.conectar()

        if cls._connection is None:
            raise RuntimeError("No se pudo abrir la conexion con la base de datos")

        return cls._connection

    @classmethod
    def obtener_columnas(cls, tabla: str = "libros") -> list[str]:
        """Devuelve las columnas de las tablas permitidas de la biblioteca."""
        if tabla not in {"libros", "generos"}:
            raise ValueError("La tabla debe ser 'libros' o 'generos'")

        filas = cls.obtener_conexion().execute(
            f"PRAGMA table_info({tabla})"
        ).fetchall()
        return [fila[1] for fila in filas]

    @classmethod
    def cerrar_conexion(cls) -> None:
        """Cierra la conexion compartida si esta abierta."""
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None

    def crear_libro(
        self,
        titulo: str,
        paginas: int,
        autor: str | None = None,
        genero_id: int | None = None,
        anio: int | None = None,
        valoracion: float | None = None,
        estado: str = "Pendiente",
        favorito: int = 0,
        notas: str | None = None,
    ) -> int:
        """Inserta un libro y devuelve su identificador."""
        sql = """
            INSERT INTO libros
                (titulo, autor, genero_id, anio, paginas, valoracion,
                 estado, favorito, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conexion = self.obtener_conexion()
        cursor = conexion.execute(
            sql,
            (titulo, autor, genero_id, anio, paginas, valoracion,
             estado, favorito, notas),
        )
        conexion.commit()
        libro_id = cursor.lastrowid
        if libro_id is None:
            raise RuntimeError("No se pudo obtener el identificador del libro")

        return libro_id

    def obtener_libro_por_id(self, libro_id: int) -> dict[str, Any] | None:
        """Devuelve un libro junto con el nombre de su genero."""
        sql = """
            SELECT l.*, g.nombre AS genero_nombre
            FROM libros AS l
            LEFT JOIN generos AS g ON l.genero_id = g.id
            WHERE l.id = ?
        """
        fila = self.obtener_conexion().execute(sql, (libro_id,)).fetchone()
        return dict(fila) if fila else None

    def obtener_todos_los_libros(
        self,
        ordenar_por: str = "id",
        descendente: bool = False,
    ) -> list[dict[str, Any]]:
        """Devuelve todos los libros ordenados por la columna indicada."""
        columnas_ordenables = {
            "id": "l.id",
            "titulo": "l.titulo",
            "autor": "l.autor",
            "genero": "g.nombre",
            "anio": "l.anio",
            "paginas": "l.paginas",
            "valoracion": "l.valoracion",
            "estado": "l.estado",
            "favorito": "l.favorito",
        }
        if ordenar_por not in columnas_ordenables:
            raise ValueError(f"Columna no ordenable: {ordenar_por}")

        direccion = "DESC" if descendente else "ASC"
        sql = """
            SELECT l.*, g.nombre AS genero_nombre
            FROM libros AS l
            LEFT JOIN generos AS g ON l.genero_id = g.id
        """ + f" ORDER BY {columnas_ordenables[ordenar_por]} {direccion}"
        filas = self.obtener_conexion().execute(sql).fetchall()
        return [dict(fila) for fila in filas]

    def actualizar_libro(self, libro_id: int, **campos: Any) -> bool:
        """Actualiza los campos indicados de un libro."""
        if not campos:
            return False

        campos_invalidos = set(campos) - self._campos_actualizables
        if campos_invalidos:
            raise ValueError(
                f"Campos no permitidos: {', '.join(sorted(campos_invalidos))}"
            )

        columnas = [f"{nombre} = ?" for nombre in campos]
        valores = list(campos.values()) + [libro_id]
        sql = f"UPDATE libros SET {', '.join(columnas)} WHERE id = ?"

        conexion = self.obtener_conexion()
        cursor = conexion.execute(sql, valores)
        conexion.commit()
        return cursor.rowcount > 0

    def eliminar_libro(self, *libro_ids: int) -> bool:
        """Elimina uno o varios libros y devuelve si existia alguno."""
        if not libro_ids:
            return False

        marcadores = ", ".join("?" for _ in libro_ids)
        sql = f"DELETE FROM libros WHERE id IN ({marcadores})"

        conexion = self.obtener_conexion()
        cursor = conexion.execute(sql, libro_ids)
        conexion.commit()
        return cursor.rowcount > 0
