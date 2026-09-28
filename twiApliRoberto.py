import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

# RECORRIDO GENERAL DEL PROGRAMA
# 1. Prepara la base de datos SQLite para guardar usuarios y publicaciones.
# 2. La clase User reúne las operaciones relacionadas con cada usuario.
# 3. La clase TwitterApp crea la ventana y conecta botones con esas operaciones.
# 4. Al final del archivo se crea la ventana y comienza el bucle de Tkinter.

# =============================================================================
# 1. BASE DE DATOS Y CONFIGURACIÓN
# =============================================================================
# La base de datos se guarda junto a este archivo, no en la carpeta de ejecución.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'twitter.db')
MAX_TWEET_LENGTH = 280

# Colores del diseño de Roberto
SIDEBAR_BG = "#0f172a"
MAIN_BG = "#f8fafc"
PRIMARY_COLOR = "#4f46e5"
TEXT_COLOR = "#1e293b"
DANGER_COLOR = "#ef4444"

def get_connection():
    """Abre la base de datos y devuelve una conexión lista para usar."""
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    # Activar Foreign Keys para borrado en cascada
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def create_db():
    """Crea las tablas necesarias si todavía no existen."""
    with get_connection() as con:
        cur = con.cursor()
        # user guarda las cuentas; tweet guarda publicaciones asociadas a una cuenta.
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                bio TEXT
            );
            CREATE TABLE IF NOT EXISTS tweet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                user_id INTEGER NOT NULL REFERENCES user (id) ON DELETE CASCADE,
                retweet_from INTEGER REFERENCES tweet (id) ON DELETE CASCADE
            );
        """)

class TwitterError(Exception):
    def __init__(self, message):
        super().__init__(message)

# =============================================================================
# 2. MODELOS DE DATOS (ESTILO ROBERTO CON @classmethod Y yield)
# =============================================================================
class User:
    """Representa una cuenta y contiene las operaciones básicas sobre ella."""
    def __init__(self, username, password="", bio="", user_id=None):
        # Estos valores quedan guardados en el objeto mientras trabaja el programa.
        self.username = username
        self.password = password
        self.bio = bio
        self.id = user_id
        self.logged = False

    @classmethod
    def from_db_row(cls, row):
        """Crea una instancia de User directamente desde una fila de SQLite."""
        if row is None:
            return None
        return cls(
            username=row["username"],
            password=row["password"],
            bio=row["bio"],
            user_id=row["id"]
        )

    @classmethod
    def get_users(cls):
        """Generador para listar todos los usuarios ordenados por ID."""
        sql = """SELECT * 
                 FROM user 
                 ORDER BY id"""
        with get_connection() as con:
            cur = con.cursor()
            res = cur.execute(sql)
            for row in res.fetchall():
                yield cls.from_db_row(row)

    def save(self):
        """Inserta el usuario o actualiza sus datos si su ID ya existe."""
        con = get_connection()
        try:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO user (id, username, password, bio)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    username = excluded.username,
                    password = excluded.password,
                    bio = excluded.bio
            """, (self.id, self.username, self.password, self.bio))
            con.commit()
            if self.id is None:
                self.id = cur.lastrowid
        finally:
            con.close()

    def login(self, password):
        """Comprueba las credenciales y marca la cuenta como conectada si coinciden."""
        with get_connection() as con:
            cur = con.cursor()
            cur.execute('SELECT id, username, bio FROM user WHERE username = ? AND password = ?',
                        (self.username, password))
            row = cur.fetchone()
            if row:
                self.id = row['id']
                self.bio = row['bio']
                self.logged = True
                return True
            return False

    def cambiar_clave(self, nueva_clave):
        with get_connection() as con:
            cur = con.cursor()
            cur.execute('UPDATE user SET password = ? WHERE id = ?', (nueva_clave, self.id))
            self.password = nueva_clave

    def eliminar_cuenta(self):
        with get_connection() as con:
            cur = con.cursor()
            cur.execute('DELETE FROM user WHERE id = ?', (self.id,))
            self.logged = False

    def tweet(self, content):
        # Antes de guardar una publicación, se comprueba sesión, texto y longitud.
        if not self.logged:
            raise TwitterError("Debes iniciar sesión.")
        content = content.strip()
        if not content:
            raise TwitterError("El tweet no puede estar vacío.")
        if len(content) > MAX_TWEET_LENGTH:
            raise TwitterError(f"Excede {MAX_TWEET_LENGTH} caracteres.")
        
        with get_connection() as con:
            cur = con.cursor()
            cur.execute('INSERT INTO tweet (content, user_id) VALUES (?,?)',
                        (content, self.id))

    def retweet(self, tweet_id):
        if not self.logged:
            raise TwitterError("Debes iniciar sesión.")
        with get_connection() as con:
            cur = con.cursor()
            cur.execute('SELECT id FROM tweet WHERE id = ?', (tweet_id,))
            if not cur.fetchone():
                raise TwitterError("El Tweet no existe.")
            cur.execute('INSERT INTO tweet (content, user_id, retweet_from) VALUES (?,?,?)',
                        ("", self.id, tweet_id))

# =============================================================================
# 3. INTERFAZ GRÁFICA (ESTILO ROBERTO - USERVAULT)
# =============================================================================
class TwitterApp:
    """Controla la ventana, sus botones y la comunicación con los datos."""
    def __init__(self, root):
        self.root = root
        self.root.title("UserVault - Twitter Manager")
        self.root.geometry("820x500")
        self.root.configure(bg=MAIN_BG)
        
        # Al iniciar, todavía no hay ningún usuario conectado.
        self.usuario_actual = None

        # Construye primero los controles y después carga los usuarios existentes.
        self._crear_menu()
        self._construir_layout()
        self._cargar_usuarios()

    # -------------------------------------------------------------------------
    # MENÚ SUPERIOR
    # -------------------------------------------------------------------------
    def _crear_menu(self):
        menubar = tk.Menu(self.root)
        
        menu_user = tk.Menu(menubar, tearoff=0)
        menu_user.add_command(label="Cambiar Contraseña", command=self._cambiar_clave)
        menu_user.add_command(label="Eliminar Mi Cuenta", command=self._eliminar_cuenta_propia)
        menu_user.add_separator()
        menu_user.add_command(label="Cerrar Sesión", command=self._logout)
        menu_user.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Ajustes de Cuenta", menu=menu_user)

        self.root.config(menu=menubar)

    # -------------------------------------------------------------------------
    # LAYOUT PRINCIPAL (Sidebar + Lado Derecho)
    # -------------------------------------------------------------------------
    def _construir_layout(self):
        # SIDEBAR (Panel Izquierdo)
        sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=155)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="UserVault", bg=SIDEBAR_BG, fg="white", 
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)

        tk.Label(
            sidebar, text="Usuarios", bg=SIDEBAR_BG, fg="#94a3b8", anchor="w"
        ).pack(fill="x", padx=22, pady=5)

        # Estado del Usuario en la Sidebar
        self.lbl_estado = tk.Label(
            sidebar, text="Estado:\nDesconectado", bg=SIDEBAR_BG, fg="#64748b", 
            font=("Segoe UI", 9, "italic"), justify="left", anchor="w"
        )
        self.lbl_estado.pack(fill="x", padx=22, pady=15)

        # CONTENIDO PRINCIPAL (Panel Derecho)
        self.main = tk.Frame(self.root, bg=MAIN_BG)
        self.main.pack(side="left", fill="both", expand=True, padx=22, pady=20)

        # Título de Sección
        tk.Label(
            self.main, text="Gestión de Usuarios", bg=MAIN_BG, fg=TEXT_COLOR, 
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        # BARRA DE BÚSQUEDA Y ACCIONES
        acciones = tk.Frame(self.main, bg=MAIN_BG)
        acciones.pack(fill="x", pady=18)

        tk.Label(acciones, text="Buscar:", bg=MAIN_BG, fg=TEXT_COLOR).pack(side="left")
        
        self.ent_buscar = tk.Entry(acciones, width=22)
        self.ent_buscar.pack(side="left", padx=(5, 5))
        self.ent_buscar.bind("<KeyRelease>", lambda e: self._cargar_usuarios())

        # Botón Buscar
        tk.Button(
            acciones, text="Buscar", bd=1, padx=8, pady=2,
            command=self._cargar_usuarios
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            acciones, text="Mostrar todos", bd=1, padx=8, pady=2,
            command=self._mostrar_todos_usuarios
        ).pack(side="left")

        # Botón Agregar Nuevo Usuario
        tk.Button(
            acciones, text="+ Agregar Usuario", bg=PRIMARY_COLOR, fg="white", 
            bd=0, padx=12, pady=6, font=("Segoe UI", 9, "bold"),
            command=self._registro_dialog
        ).pack(side="right")

        # TABLA DE USUARIOS (TREEVIEW)
        frame_tabla = ttk.Frame(self.main)
        frame_tabla.pack(fill="both", expand=True)

        self.tabla_usuarios = ttk.Treeview(
            frame_tabla, columns=("id", "usuario", "password", "bio"),
            show="headings", selectmode="extended"
        )
        self.tabla_usuarios.heading("id", text="ID")
        self.tabla_usuarios.heading("usuario", text="Usuario")
        self.tabla_usuarios.heading("password", text="Contraseña")
        self.tabla_usuarios.heading("bio", text="Biografía")

        self.tabla_usuarios.column("id", width=45, anchor="center")
        self.tabla_usuarios.column("usuario", width=160)
        self.tabla_usuarios.column("password", width=120)
        self.tabla_usuarios.column("bio", width=220)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tabla_usuarios.pack(fill="both", expand=True)

        # BOTONES INFERIORES DE ACCIÓN
        botones = tk.Frame(self.main, bg=MAIN_BG)
        botones.pack(fill="x", pady=15)

        tk.Button(
            botones, text="Eliminar", bg=DANGER_COLOR, fg="white", 
            bd=0, padx=12, pady=6, command=self._eliminar_usuario_tabla
        ).pack(side="left", padx=3)

        tk.Button(
            botones, text="Editar Seleccionado", bd=1, padx=10, pady=5, height=2,
            command=self._editar_usuario_seleccionado
        ).pack(side="left", padx=3)

    # -------------------------------------------------------------------------
    # MÉTODOS DE DATOS Y LÓGICA
    # -------------------------------------------------------------------------
    def _cargar_usuarios(self):
        """Vacía la tabla y vuelve a cargar usuarios que coincidan con la búsqueda."""
        # Se borran las filas antiguas para evitar duplicados al actualizar la vista.
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        criterio_busqueda = self.ent_buscar.get().strip().lower()

        # Recorremos la función generadora User.get_users()
        for user in User.get_users():
            # Filtro por coincidencia con el criterio de búsqueda
            if criterio_busqueda and criterio_busqueda not in user.username.lower():
                continue

            self.tabla_usuarios.insert(
                "", "end", 
                values=(user.id, user.username, user.password, user.bio or "")
            )

    def _mostrar_todos_usuarios(self):
        """Limpia el filtro de búsqueda y muestra todos los usuarios."""
        self.ent_buscar.delete(0, tk.END)
        self._cargar_usuarios()

    def _login_desde_tabla(self):
        """Inicia sesión con el usuario seleccionado en la tabla."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return messagebox.showwarning("Atención", "Selecciona un usuario de la tabla.")
        
        valores = self.tabla_usuarios.item(seleccion[0], "values")
        username_sel = valores[1]
        pass_sel = valores[2]

        user = User(username_sel)
        if user.login(pass_sel):
            self.usuario_actual = user
            self.lbl_estado.config(text=f"Conectado:\n@{user.username}", fg="#22c55e")
            messagebox.showinfo("Login", f"¡Sesión iniciada como @{user.username}!")
        else:
            messagebox.showerror("Error", "No se pudo iniciar sesión.")

    def _logout(self):
        """Cierra la sesión del usuario activo."""
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "No hay ninguna sesión activa.")
        
        self.usuario_actual = None
        self.lbl_estado.config(text="Estado:\nDesconectado", fg="#64748b")
        messagebox.showinfo("Sesión", "Has cerrado sesión correctamente.")

    def _guardar_usuario_formulario(
        self, ventana, modo, user_id, ent_nombre, ent_clave, ent_bio
    ):
        """Guarda un usuario nuevo o actualiza uno existente desde un formulario."""
        nombre = ent_nombre.get().strip()
        clave = ent_clave.get().strip()
        bio = ent_bio.get().strip()

        if not nombre or not clave:
            return messagebox.showwarning(
                "Atención", "El nombre y la clave son obligatorios.", parent=ventana
            )

        try:
            usuario = User(
                username=nombre,
                password=clave,
                bio=bio,
                user_id=user_id if modo == "editar" else None
            )
            usuario.save()

            if (
                modo == "editar"
                and self.usuario_actual
                and self.usuario_actual.id == int(user_id)
            ):
                self.usuario_actual.username = nombre
                self.usuario_actual.password = clave
                self.usuario_actual.bio = bio

            ventana.destroy()
            self._cargar_usuarios()
            messagebox.showinfo(
                "Éxito", "Operación realizada correctamente.", parent=self.root
            )
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error", "El nombre de usuario ya existe.", parent=ventana
            )
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"No se pudo guardar: {e}", parent=ventana
            )

    def _registro_dialog(self):
        """Abre un formulario modal para crear un usuario."""
        # Toplevel crea una ventana secundaria; grab_set hace que sea modal.
        ventana_nuevo = tk.Toplevel(self.root)
        ventana_nuevo.title("Crear Nuevo Usuario")
        ventana_nuevo.geometry("380x280")
        ventana_nuevo.resizable(False, False)
        ventana_nuevo.transient(self.root)
        ventana_nuevo.grab_set()

        tk.Label(ventana_nuevo, text="Nombre:").place(x=20, y=20)
        ent_nombre = tk.Entry(ventana_nuevo, width=30)
        ent_nombre.place(x=100, y=20)

        tk.Label(ventana_nuevo, text="Clave:").place(x=20, y=60)
        ent_clave = tk.Entry(ventana_nuevo, width=30, show="*")
        ent_clave.place(x=100, y=60)

        tk.Label(ventana_nuevo, text="Biografía:").place(x=20, y=100)
        ent_bio = tk.Entry(ventana_nuevo, width=30)
        ent_bio.place(x=100, y=100)

        tk.Label(
            ventana_nuevo,
            text="Clave: @ o =, 2-4 dígitos,\n2-4 letras, ! o *, por ejemplo @12Ab!",
            justify="left",
            fg="gray"
        ).place(x=20, y=135)

        def guardar_nuevo_usuario():
            self._guardar_usuario_formulario(
                ventana_nuevo, "nuevo", None, ent_nombre, ent_clave, ent_bio
            )

        tk.Button(
            ventana_nuevo, text="Guardar cambios", bg="#4F46E5", fg="white",
            command=guardar_nuevo_usuario
        ).place(x=20, y=210, width=120, height=35)

        tk.Button(
            ventana_nuevo, text="Cancelar", command=ventana_nuevo.destroy
        ).place(x=150, y=210, width=80, height=35)

        ent_nombre.focus_set()

    def _eliminar_usuario_tabla(self):
        """Elimina todos los usuarios seleccionados en la tabla."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return messagebox.showwarning(
                "Atención",
                "Por favor, selecciona al menos un usuario para eliminar.",
                parent=self.root
            )

        usuarios_a_eliminar = []
        ids_a_eliminar = []
        for item in seleccion:
            valores = self.tabla_usuarios.item(item, "values")
            user_id = int(valores[0])
            username = valores[1]
            ids_a_eliminar.append(user_id)
            usuarios_a_eliminar.append(f"ID {user_id}: {username}")

        cantidad = len(ids_a_eliminar)
        lista_texto = "\n".join(usuarios_a_eliminar)
        if cantidad == 1:
            mensaje = (
                "¿Eliminar al siguiente usuario y todos sus tweets?\n\n"
                f"{lista_texto}"
            )
        else:
            mensaje = (
                f"¿Eliminar a estos {cantidad} usuarios y todos sus tweets?\n\n"
                f"{lista_texto}"
            )

        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            mensaje,
            parent=self.root
        )
        if not confirmacion:
            return

        try:
            with get_connection() as con:
                cur = con.cursor()
                placeholders = ",".join("?" for _ in ids_a_eliminar)
                # Se eliminan primero las publicaciones para respetar las claves foráneas.
                cur.execute(
                    f"DELETE FROM tweet WHERE user_id IN ({placeholders})",
                    ids_a_eliminar
                )
                cur.execute(
                    f"DELETE FROM user WHERE id IN ({placeholders})",
                    ids_a_eliminar
                )

            if self.usuario_actual and self.usuario_actual.id in ids_a_eliminar:
                self.usuario_actual.logged = False
                self.usuario_actual = None
                self.lbl_estado.config(text="Estado:\nDesconectado", fg="#64748b")

            self._cargar_usuarios()
            messagebox.showinfo(
                "Éxito",
                f"Se eliminaron {cantidad} usuario(s) y sus publicaciones.",
                parent=self.root
            )
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"No se pudieron eliminar los usuarios: {e}",
                parent=self.root
            )

    def _editar_usuario_seleccionado(self):
        """Edita los datos del usuario seleccionado en la tabla."""
        # Primero se necesita una fila seleccionada para saber qué cuenta editar.
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return messagebox.showwarning(
                "Atención", "Por favor, selecciona un usuario de la lista."
            )

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        user_id, username_actual, password_actual, bio_actual = valores

        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title(f"Editar usuario: {username_actual}")
        ventana_editar.geometry("380x280")
        ventana_editar.resizable(False, False)
        ventana_editar.transient(self.root)
        ventana_editar.grab_set()

        tk.Label(ventana_editar, text="Nombre:").place(x=20, y=20)
        ent_nombre = tk.Entry(ventana_editar, width=30)
        ent_nombre.insert(0, username_actual)
        ent_nombre.place(x=100, y=20)

        tk.Label(ventana_editar, text="Clave:").place(x=20, y=60)
        ent_clave = tk.Entry(ventana_editar, width=30, show="*")
        ent_clave.insert(0, password_actual)
        ent_clave.place(x=100, y=60)

        tk.Label(ventana_editar, text="Biografía:").place(x=20, y=100)
        ent_bio = tk.Entry(ventana_editar, width=30)
        ent_bio.insert(0, bio_actual)
        ent_bio.place(x=100, y=100)

        tk.Label(
            ventana_editar,
            text="Clave: @ o =, 2-4 dígitos,\n2-4 letras, ! o *, por ejemplo @12Ab!",
            justify="left",
            fg="gray"
        ).place(x=20, y=135)

        def guardar_cambios():
            self._guardar_usuario_formulario(
                ventana_editar, "editar", int(user_id),
                ent_nombre, ent_clave, ent_bio
            )

        tk.Button(
            ventana_editar, text="Guardar cambios", bg="#4F46E5", fg="white",
            command=guardar_cambios
        ).place(x=20, y=210, width=120, height=35)

        tk.Button(
            ventana_editar, text="Cancelar", command=ventana_editar.destroy
        ).place(x=150, y=210, width=80, height=35)

    def _cambiar_clave(self):
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "Inicia sesión primero.")
        nueva = simpledialog.askstring("Cambiar Clave", "Introduce tu nueva contraseña:", show="*")
        if nueva:
            self.usuario_actual.cambiar_clave(nueva)
            self._cargar_usuarios()
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")

    def _eliminar_cuenta_propia(self):
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "Inicia sesión primero.")
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres eliminar tu cuenta activa?"):
            self.usuario_actual.eliminar_cuenta()
            self._logout()
            self._cargar_usuarios()
            messagebox.showinfo("Cuenta Eliminada", "Tu cuenta se ha borrado con éxito.")

# =============================================================================
# 4. EJECUCIÓN
# =============================================================================
if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando se lanza este archivo directamente.
    # 1. Prepara SQLite. 2. Crea la ventana. 3. Mantiene la interfaz abierta.
    create_db()
    root = tk.Tk()
    app = TwitterApp(root)
    root.mainloop()