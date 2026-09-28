import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

# =============================================================================
# 1. BASE DE DATOS Y CONFIGURACIÓN
# =============================================================================
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'twitter.db')
MAX_TWEET_LENGTH = 280

def get_connection():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def create_db():
    with get_connection() as con:
        cur = con.cursor()
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
    pass

# =============================================================================
# 2. MODELOS DE DATOS
# =============================================================================
class User:
    def __init__(self, username, password="", bio="", user_id=0):
        self.username = username
        self.password = password
        self.bio = bio
        self.id = user_id
        self.logged = False

    def save(self):
        with get_connection() as con:
            cur = con.cursor()
            cur.execute('INSERT INTO user (username, password, bio) VALUES (?,?,?)',
                        (self.username, self.password, self.bio))
            self.id = cur.lastrowid

    def login(self, password):
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
# 3. INTERFAZ GRÁFICA AVANZADA
# =============================================================================
class TwitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitter KASIO Pro Edition")
        self.root.geometry("550x600")
        
        self.usuario_actual = None

        self._crear_menu()
        
        # Estado de Usuario
        self.lbl_estado = tk.Label(root, text="Estado: Desconectado", bg="#333", fg="white", font=("Arial", 10, "bold"), pady=5)
        self.lbl_estado.pack(fill=tk.X)

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_auth = ttk.Frame(self.notebook)
        self.tab_tweet = ttk.Frame(self.notebook)
        self.tab_rt = ttk.Frame(self.notebook)
        self.tab_timeline = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_auth, text="Cuenta")
        self.notebook.add(self.tab_tweet, text="Publicar Tweet")
        self.notebook.add(self.tab_rt, text="Retweet")
        self.notebook.add(self.tab_timeline, text="Timeline Feed")

        self._build_auth_tab()
        self._build_tweet_tab()
        self._build_rt_tab()
        self._build_timeline_tab()

    # -------------------------------------------------------------------------
    # MENÚ SUPERIOR (Ajustes de Cuenta)
    # -------------------------------------------------------------------------
    def _crear_menu(self):
        menubar = tk.Menu(self.root)
        
        menu_user = tk.Menu(menubar, tearoff=0)
        menu_user.add_command(label="Cambiar Contraseña", command=self._cambiar_clave)
        menu_user.add_command(label="Eliminar Mi Cuenta", command=self._eliminar_cuenta)
        menu_user.add_command(label="Cerrar Sesión", command=self._logout)
        menu_user.add_separator()
        menu_user.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Ajustes de Cuenta", menu=menu_user)

        self.root.config(menu=menubar)

    # -------------------------------------------------------------------------
    # PESTAÑA: CUENTA
    # -------------------------------------------------------------------------
    def _build_auth_tab(self):
        lf = ttk.LabelFrame(self.tab_auth, text=" Gestión de Usuario ", padding=15)
        lf.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(lf, text="Usuario:").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_user = ttk.Entry(lf)
        self.ent_user.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(lf, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_pass = ttk.Entry(lf, show="*")
        self.ent_pass.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(lf, text="Bio:").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_bio = ttk.Entry(lf)
        self.ent_bio.grid(row=2, column=1, sticky="ew", pady=5)

        lf.columnconfigure(1, weight=1)

        btn_box = ttk.Frame(lf)
        btn_box.grid(row=3, column=0, columnspan=2, pady=15)

        ttk.Button(btn_box, text="Iniciar Sesión", command=self._login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Crear Nuevo Usuario", command=self._registro).pack(side=tk.LEFT, padx=5)

    # -------------------------------------------------------------------------
    # PESTAÑA: PUBLICAR TWEET
    # -------------------------------------------------------------------------
    def _build_tweet_tab(self):
        lf = ttk.LabelFrame(self.tab_tweet, text=" ¿Qué está pasando? ", padding=10)
        lf.pack(padx=10, pady=10, fill="both", expand=True)

        self.txt_tweet = tk.Text(lf, height=6)
        self.txt_tweet.pack(fill="both", expand=True, pady=5)

        ttk.Button(lf, text="🚀 Publicar Tweet", command=self._publicar_tweet).pack(pady=10)

    # -------------------------------------------------------------------------
    # PESTAÑA: RETWEET
    # -------------------------------------------------------------------------
    def _build_rt_tab(self):
        lf = ttk.LabelFrame(self.tab_rt, text=" Retweetear ", padding=15)
        lf.pack(padx=10, pady=10, fill="x")

        ttk.Label(lf, text="ID del Tweet a re-twitear:").pack(side=tk.LEFT, padx=5)
        self.ent_rt_id = ttk.Entry(lf, width=10)
        self.ent_rt_id.pack(side=tk.LEFT, padx=5)

        ttk.Button(lf, text="Hacer Retweet", command=self._hacer_retweet).pack(side=tk.LEFT, padx=5)

    # -------------------------------------------------------------------------
    # PESTAÑA: TIMELINE FEED
    # -------------------------------------------------------------------------
    def _build_timeline_tab(self):
        top_bar = ttk.Frame(self.tab_timeline)
        top_bar.pack(fill="x", padx=10, pady=5)

        ttk.Button(top_bar, text="🔄 Actualizar Feed", command=self._cargar_timeline).pack(side=tk.LEFT)
        ttk.Button(top_bar, text="🗑️ Borrar Tweet Propio", command=self._borrar_tweet).pack(side=tk.RIGHT)

        frame_list = ttk.Frame(self.tab_timeline)
        frame_list.pack(padx=10, pady=5, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_list)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_tweets = tk.Listbox(frame_list, font=("Arial", 10), bd=2, yscrollcommand=scrollbar.set)
        self.listbox_tweets.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.listbox_tweets.yview)

    # -------------------------------------------------------------------------
    # ACCIONES Y EVENTOS
    # -------------------------------------------------------------------------
    def _login(self):
        user = User(self.ent_user.get().strip())
        if user.login(self.ent_pass.get().strip()):
            self.usuario_actual = user
            self.lbl_estado.config(text=f"Conectado como: @{user.username}", bg="#2eb82e")
            messagebox.showinfo("Login", f"¡Bienvenido @{user.username}!")
            self._cargar_timeline()
            self.notebook.select(self.tab_timeline)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def _logout(self):
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "No hay ninguna sesión activa")
        
        # 1. Reseteamos el objeto de usuario activo a None
        self.usuario_actual = None
        
        # 2. Restauramos la etiqueta visual de estado
        self.lbl_estado.config(text="Estado: Desconectado", bg="#333")
        
        # 3. Limpiamos las cajas de texto de login por seguridad
        self.ent_pass.delete(0, tk.END)
        self.ent_user.delete(0, tk.END)
        
        # 4. Volvemos a la pestaña principal de cuenta
        self.notebook.select(self.tab_auth)
        
        messagebox.showinfo("Sesión", "Has cerrado sesión correctamente.")

    def _registro(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        b = self.ent_bio.get().strip()
        if not u or not p:
            messagebox.showwarning("Atención", "Rellena usuario y contraseña")
            return
        try:
            User(u, p, b).save()
            messagebox.showinfo("Éxito", "Usuario creado correctamente")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe")

    def _cambiar_clave(self):
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "Inicia sesión primero")
        nueva = simpledialog.askstring("Cambiar Clave", "Introduce tu nueva contraseña:", show="*")
        if nueva:
            self.usuario_actual.cambiar_clave(nueva)
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente")

    def _eliminar_cuenta(self):
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "Inicia sesión primero")
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres eliminar tu cuenta y todos tus tweets?"):
            self.usuario_actual.eliminar_cuenta()
            
            # Reemplazas self.usuario_actual = None y self.lbl_estado.config(...) por esto:
            self._logout()
            
            messagebox.showinfo("Cuenta Eliminada", "Tu cuenta se ha borrado con éxito.")
    def _publicar_tweet(self):
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "Inicia sesión primero")
        txt = self.txt_tweet.get("1.0", tk.END).strip()
        try:
            self.usuario_actual.tweet(txt)
            messagebox.showinfo("Publicado", "¡Tweet enviado!")
            self.txt_tweet.delete("1.0", tk.END)
            self._cargar_timeline()
            self.notebook.select(self.tab_timeline)
        except TwitterError as e:
            messagebox.showerror("Error", str(e))

    def _hacer_retweet(self):
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "Inicia sesión primero")
        tweet_id_str = self.ent_rt_id.get().strip()
        if not tweet_id_str.isdigit():
            return messagebox.showerror("Error", "Introduce un ID numérico válido")
        try:
            self.usuario_actual.retweet(int(tweet_id_str))
            messagebox.showinfo("Retweet", "¡Retweet realizado con éxito!")
            self.ent_rt_id.delete(0, tk.END)
            self._cargar_timeline()
            self.notebook.select(self.tab_timeline)
        except TwitterError as e:
            messagebox.showerror("Error", str(e))

    def _cargar_timeline(self):
        self.listbox_tweets.delete(0, tk.END)
        with get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT t.id, t.content, t.retweet_from, u.username 
                FROM tweet t JOIN user u ON t.user_id = u.id ORDER BY t.id DESC
            """)
            for row in cur.fetchall():
                prefix = "[RT] " if row['retweet_from'] else ""
                contenido = row['content']
                if row['retweet_from']:
                    cur.execute("SELECT content FROM tweet WHERE id = ?", (row['retweet_from'],))
                    orig = cur.fetchone()
                    contenido = orig['content'] if orig else "[Tweet borrado]"

                self.listbox_tweets.insert(
                    tk.END, f"[{row['id']}] @{row['username']}: {prefix}{contenido}"
                )

    def _borrar_tweet(self):
        if not self.usuario_actual:
            return messagebox.showwarning("Atención", "Inicia sesión primero")
        t_id = simpledialog.askinteger("Borrar Tweet", "Introduce el ID del Tweet a eliminar:")
        if t_id:
            with get_connection() as con:
                cur = con.cursor()
                cur.execute("DELETE FROM tweet WHERE id = ? AND user_id = ?", (t_id, self.usuario_actual.id))
                if cur.rowcount > 0:
                    messagebox.showinfo("Éxito", "Tweet eliminado")
                    self._cargar_timeline()
                else:
                    messagebox.showerror("Error", "No se pudo borrar (comprueba si el tweet es tuyo o si el ID existe)")

if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    app = TwitterApp(root)
    root.mainloop()