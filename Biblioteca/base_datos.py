"""Creación de la base de datos SQLite de la biblioteca."""

import sqlite3
from pathlib import Path

RUTA_BASE_DATOS = Path(__file__).resolve().parent / "biblioteca.db"

conexion = sqlite3.connect(RUTA_BASE_DATOS)
cursor = conexion.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute(
	"""
	CREATE TABLE IF NOT EXISTS generos (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT NOT NULL UNIQUE
	)
	"""
)

cursor.execute(
	"""
	CREATE TABLE IF NOT EXISTS libros (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		titulo TEXT NOT NULL,
		autor TEXT,
		genero_id INTEGER,
		anio INTEGER CHECK (anio >= 1440),
		paginas INTEGER NOT NULL CHECK (paginas > 50),
		valoracion REAL CHECK (valoracion >= 0 AND valoracion <= 10),
		estado TEXT NOT NULL DEFAULT 'Pendiente'
			CHECK (estado IN ('Pendiente', 'Leyendo', 'Terminado')),
		favorito INTEGER CHECK (favorito IN (0, 1)),
		notas TEXT CHECK (LENGTH(notas) <= 500),
		FOREIGN KEY (genero_id) REFERENCES generos(id)
	)
	"""
)

cursor.execute("DROP TRIGGER IF EXISTS validar_anio_al_insertar")
cursor.execute("DROP TRIGGER IF EXISTS validar_anio_al_modificar")

cursor.execute(
	"""
	CREATE TRIGGER IF NOT EXISTS check_fecha_before_insert
	BEFORE INSERT ON libros
	FOR EACH ROW
	BEGIN
		SELECT RAISE(ABORT, 'El año no puede ser futuro')
		WHERE NEW.anio > CAST(strftime('%Y', 'now') AS INTEGER);
	END
	"""
)

cursor.execute(
	"""
	CREATE TRIGGER IF NOT EXISTS check_fecha_before_update
	BEFORE UPDATE ON libros
	FOR EACH ROW
	BEGIN
		SELECT RAISE(ABORT, 'El año no puede ser futuro')
		WHERE NEW.anio > CAST(strftime('%Y', 'now') AS INTEGER);
	END
	"""
)

conexion.commit()
conexion.close()