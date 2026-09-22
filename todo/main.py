from __future__ import annotations

import sqlite3

DB_PATH = "todo.db"


def create_db(db_path: str = DB_PATH) -> None:
    """Crea la base de datos y la tabla tasks en la ruta indicada."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
            """
        )


class Task:
    def __init__(self, name: str, done: bool = False, id: int = -1):
        self.name = name
        self.done = done
        self.id = id

    def _get_connection(self):
        return self.__class__.con

    def save(self) -> None:
        """Inserta la tarea en la BD y asigna su ID generado."""
        with self._get_connection() as con:
            cur = con.cursor()
            query = "INSERT INTO tasks (name, done) VALUES (?, ?)"
            cur.execute(query, (self.name, self.done))
            con.commit()
            self.id = cur.lastrowid

    def update(self) -> None:
        """Actualiza el nombre y estado de la tarea en la BD."""
        with self._get_connection() as con:
            cur = con.cursor()
            query = "UPDATE tasks SET name = ?, done = ? WHERE id = ?"
            cur.execute(query, (self.name, self.done, self.id))
            con.commit()

    def check(self) -> None:
        """Marca la tarea como completada y la actualiza en la BD."""
        self.done = True
        self.update()

    def uncheck(self) -> None:
        """Marca la tarea como no completada y la actualiza en la BD."""
        self.done = False
        self.update()

    def __repr__(self):
        status = "X" if self.done else " "
        return f"[{status}] {self.name} (id={self.id})"

    @classmethod
    def from_db_row(cls, row: sqlite3.Row) -> "Task":
        """Construye y devuelve una nueva tarea desde una fila sqlite3.Row."""
        return cls(name=row["name"], done=bool(row["done"]), id=row["id"])

    @classmethod
    def get(cls, task_id: int) -> "Task | None":
        """Obtiene una tarea desde la BD según su ID utilizando from_db_row."""
        query = "SELECT id, name, done FROM tasks WHERE id = ?"
        row = cls.con.execute(query, (task_id,)).fetchone()
        return None if row is None else cls.from_db_row(row)


class ToDo:
    def _get_connection(self):
        return self.__class__.con

    def get_tasks(self, done: int = -1):
        """Función generadora que devuelve instancias de Task según su estado."""
        if done == -1:
            query = "SELECT id, name, done FROM tasks"
            params = ()
        else:
            query = "SELECT id, name, done FROM tasks WHERE done = ?"
            params = (done,)

        for row in self._get_connection().execute(query, params):
            yield Task.from_db_row(row)

    def add_task(self, name: str) -> None:
        """Añade una nueva tarea delegando en la clase Task."""
        task = Task(name=name)
        task.save()

    def complete_task(self, task_id: int) -> None:
        """Marca como completada la tarea con el ID indicado."""
        task = Task.get(task_id)
        if task:
            task.check()

    def reopen_task(self, task_id: int) -> None:
        """Marca como pendiente la tarea con el ID indicado."""
        task = Task.get(task_id)
        if task:
            task.uncheck()


for class_ in (Task, ToDo):
    class_.con = sqlite3.connect(DB_PATH)
    class_.con.row_factory = sqlite3.Row
    class_.cur = class_.con.cursor()