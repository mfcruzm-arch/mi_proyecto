import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# =============================================================================
# 1. CONSTANTES Y CONFIGURACIÓN BASE DE LA DB
# =============================================================================
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'twitter.db')
MAX_TWEET_LENGTH = 280
RETWEET_PREFIX = '[RT]'


def conexion_db(db_path=DB_PATH):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur


def create_db(db_path: str = DB_PATH) -> None:
    """Crea la base de datos y las tablas si no existen."""
    con, cur = conexion_db(db_path)
    sql = """
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


class TwitterError(Exception):

    def __init__(self, message):
        super().__init__(message)


# =============================================================================
# 2. MODELOS DE DATOS (ESTILO DE ROBERTO)
# =============================================================================
class User:

    def __init__(
        self, username: str, password: str, bio: str = '', user_id: int = 0
    ):
        self.con, self.cur = conexion_db(DB_PATH)
        self.username = username
        self.password = password
        self.bio = bio
        self.id = user_id
        self.logged: bool = False

    def save(self) -> None:
        sql = 'INSERT INTO user (username, password, bio) VALUES (?,?,?)'
        self.cur.execute(sql, (self.username, self.password, self.bio))
        self.id = self.cur.lastrowid
        self.con.commit()

    def login(self, password: str) -> bool:
        sql = """SELECT id, username, bio, password
               FROM user
               WHERE username = ? AND password = ?"""
        res = self.cur.execute(sql, (self.username, password))
        row = res.fetchone()
        if row:
            self.id = row['id']
            self.bio = row['bio']
            self.logged = True
            self.con.commit()
            return True
        self.logged = False
        return False

    def tweet(self, content: str) -> 'Tweet':
        if not self.logged:
            raise TwitterError(f'El usuario {self.username} no ha iniciado sesión.')
        if len(content) > MAX_TWEET_LENGTH:
            raise TwitterError(
                f'El tweet supera el límite de {MAX_TWEET_LENGTH} caracteres.'
            )

        nuevo_tweet = Tweet(content=content)
        nuevo_tweet.save(self)
        return nuevo_tweet

    def retweet(self, tweet_id: int) -> 'Tweet':
        if not self.logged:
            raise TwitterError(f'El usuario {self.username} no ha iniciado sesión.')

        sql = 'SELECT id FROM tweet WHERE id = ?'
        res = self.cur.execute(sql, (tweet_id,))
        if res.fetchone() is None:
            raise TwitterError(f'El tweet ID {tweet_id} no existe.')

        nuevo_rt = Tweet(retweet_from=tweet_id)
        nuevo_rt.save(self)
        return nuevo_rt

    @classmethod
    def tweets(cls) -> list['Tweet']:
        con, cur = conexion_db(DB_PATH)
        sql = 'SELECT id, content, user_id, retweet_from FROM tweet ORDER BY id DESC'
        res = cur.execute(sql)
        rows = res.fetchall()
        con.close()
        return [Tweet.from_db_row(row) for row in rows]


class Tweet:

    def __init__(
        self, content: str = '', retweet_from: int = 0, tweet_id: int = 0
    ):
        self.con, self.cur = conexion_db(DB_PATH)
        self.retweet_from = retweet_from
        self.id = tweet_id
        # Corrección lógica de Roberto: contenido solo si NO es retweet
        self._content = content if retweet_from == 0 else ''

    @property
    def is_retweet(self) -> bool:
        return bool(self.retweet_from)

    @property
    def content(self) -> str:
        if not self.is_retweet:
            return self._content
        else:
            sql = 'SELECT content FROM tweet WHERE id = ?'
            res = self.cur.execute(sql, (self.retweet_from,))
            row = res.fetchone()
            return row['content'] if row else '[Tweet borrado]'

    def save(self, user: User) -> None:
        sql = 'INSERT INTO tweet (content, user_id, retweet_from) VALUES (?,?,?)'
        self.cur.execute(sql, (self._content, user.id, self.retweet_from))
        self.id = self.cur.lastrowid
        self.con.commit()

    def __repr__(self):
        prefijo = f'{RETWEET_PREFIX} ' if self.is_retweet else ''
        return f'{prefijo}{self.content} (id={self.id})'

    @classmethod
    def from_db_row(cls, row: sqlite3.Row) -> 'Tweet':
        return cls(
            content=row['content'],
            retweet_from=row['retweet_from'] or 0,
            tweet_id=row['id'],
        )


# =============================================================================
# 3. INTERFAZ GRÁFICA CON TKINTER (CLASE PRINCIPAL)
# =============================================================================
class TwitterApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Twitter KASIO Edition")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        # Estado de sesión
        self.usuario_actual = None

        # Encabezado / Estado de Usuario
        self.label_estado = tk.Label(
            root,
            text="Estado: Sin conexión",
            font=("Arial", 11, "bold"),
            bg="#333333",
            fg="white",
            anchor="w",
            padx=10,
        )
        self.label_estado.pack(side=tk.TOP, fill=tk.X)

        # Contenedor de Pestañas (Notebook)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Inicialización de Pestañas
        self.tab_auth = ttk.Frame(self.notebook)
        self.tab_tweet = ttk.Frame(self.notebook)
        self.tab_rt = ttk.Frame(self.notebook)
        self.tab_timeline = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_auth, text="Autenticación")
        self.notebook.add(self.tab_tweet, text="Publicar")
        self.notebook.add(self.tab_rt, text="Retweet")
        self.notebook.add(self.tab_timeline, text="Timeline")

        # Construcción de secciones
        self._crear_tab_auth()
        self._crear_tab_tweet()
        self._crear_tab_rt()
        self._crear_tab_timeline()

    # -------------------------------------------------------------------------
    # PESTAÑA 1: AUTENTICACIÓN (LOGIN Y REGISTRO)
    # -------------------------------------------------------------------------
    def _crear_tab_auth(self):
        frame = tk.LabelFrame(
            self.tab_auth, text=" Datos de Usuario ", padx=15, pady=15
        )
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(frame, text="Usuario:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_user = tk.Entry(frame)
        self.entry_user.grid(row=0, column=1, sticky="ew", pady=5)  # CORREGIDO

        tk.Label(frame, text="Contraseña:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_pass = tk.Entry(frame, show="*")
        self.entry_pass.grid(row=1, column=1, sticky="ew", pady=5)  # CORREGIDO

        tk.Label(frame, text="Bio (Registro):").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.entry_bio = tk.Entry(frame)
        self.entry_bio.grid(row=2, column=1, sticky="ew", pady=5)  # CORREGIDO

        frame.grid_columnconfigure(1, weight=1)

        # Botones
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(
            btn_frame,
            text="Iniciar Sesión",
            bg="#4ecdc4",
            fg="white",
            command=self._login,
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            btn_frame,
            text="Registrar",
            bg="#1da1f2",
            fg="white",
            command=self._registro,
        ).pack(side=tk.LEFT, padx=5)

    def _login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        user = User(username=username, password=password)
        if user.login(password):
            self.usuario_actual = user
            self.label_estado.config(
                text=f"Conectado como: @{user.username}", bg="#2eb82e"
            )
            messagebox.showinfo(
                "Login Correcto", f"Bienvenido/a @{user.username}"
            )
        else:
            messagebox.showerror(
                "Error de Login", "Credenciales incorrectas."
            )

    def _registro(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        bio = self.entry_bio.get().strip()

        if not username or not password:
            messagebox.showwarning(
                "Campos vacíos", "Introduce usuario y contraseña."
            )
            return

        try:
            nuevo_usuario = User(username, password, bio)
            nuevo_usuario.save()
            messagebox.showinfo(
                "Éxito", f"Usuario @{username} creado correctamente."
            )
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")

    # -------------------------------------------------------------------------
    # PESTAÑA 2: PUBLICAR TWEET
    # -------------------------------------------------------------------------
    def _crear_tab_tweet(self):
        tk.Label(
            self.tab_tweet,
            text="¿Qué está pasando?",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=10, pady=5)

        self.txt_tweet = tk.Text(self.tab_tweet, height=6, width=40)
        self.txt_tweet.pack(padx=10, pady=5, fill="both", expand=True)

        tk.Button(
            self.tab_tweet,
            text="Publicar Tweet",
            bg="#1da1f2",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self._publicar_tweet,
        ).pack(pady=10)

    def _publicar_tweet(self):
        if not self.usuario_actual or not self.usuario_actual.logged:
            messagebox.showwarning(
                "Atención", "Debes iniciar sesión primero."
            )
            return

        contenido = self.txt_tweet.get("1.0", tk.END).strip()
        try:
            self.usuario_actual.tweet(contenido)
            messagebox.showinfo("Tweet", "¡Tweet publicado con éxito!")
            self.txt_tweet.delete("1.0", tk.END)
            self._actualizar_timeline()
        except TwitterError as e:
            messagebox.showerror("Error de Twitter", str(e))

    # -------------------------------------------------------------------------
    # PESTAÑA 3: RETWEET
    # -------------------------------------------------------------------------
    def _crear_tab_rt(self):
        frame = tk.Frame(self.tab_rt, padx=15, pady=15)
        frame.pack(fill="x")

        tk.Label(frame, text="ID del Tweet a re-twitear:").pack(
            side=tk.LEFT, padx=5
        )
        self.entry_rt_id = tk.Entry(frame, width=10)
        self.entry_rt_id.pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame,
            text="Hacer Retweet",
            bg="#f0a500",
            fg="white",
            command=self._hacer_retweet,
        ).pack(side=tk.LEFT, padx=5)

    def _hacer_retweet(self):
        if not self.usuario_actual or not self.usuario_actual.logged:
            messagebox.showwarning(
                "Atención", "Debes iniciar sesión primero."
            )
            return

        tweet_id_str = self.entry_rt_id.get().strip()
        if not tweet_id_str.isdigit():
            messagebox.showerror(
                "Error", "Introduce un número de ID válido."
            )
            return

        try:
            self.usuario_actual.retweet(int(tweet_id_str))
            messagebox.showinfo("Retweet", "¡Retweet realizado con éxito!")
            self.entry_rt_id.delete(0, tk.END)
            self._actualizar_timeline()
        except TwitterError as e:
            messagebox.showerror("Error de Twitter", str(e))

    # -------------------------------------------------------------------------
    # PESTAÑA 4: TIMELINE (FEED DE TWEETS)
    # -------------------------------------------------------------------------
    def _crear_tab_timeline(self):
        self.listbox_tweets = tk.Listbox(
            self.tab_timeline, font=("Arial", 10), bd=2
        )
        self.listbox_tweets.pack(
            padx=10, pady=10, fill="both", expand=True
        )

        tk.Button(
            self.tab_timeline,
            text="Actualizar Timeline",
            command=self._actualizar_timeline,
        ).pack(pady=5)

    def _actualizar_timeline(self):
        self.listbox_tweets.delete(0, tk.END)
        lista_tweets = User.tweets()
        for t in lista_tweets:
            self.listbox_tweets.insert(tk.END, str(t))


# =============================================================================
# INICIALIZACIÓN DE LA APLICACIÓN
# =============================================================================
if __name__ == "__main__":
    create_db(DB_PATH)  # Garantiza que existan la DB y las tablas
    root = tk.Tk()
    app = TwitterApp(root)
    root.mainloop()