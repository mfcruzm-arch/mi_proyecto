"""Interfaz UserVault para administrar las cuentas de ApliTwiRob."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from aplicacion import TwitterApplication
from modelo import TwitterError, create_db


SIDEBAR_BG = "#0f172a"
MAIN_BG = "#f8fafc"
PRIMARY_COLOR = "#4f46e5"
TEXT_COLOR = "#1e293b"
DANGER_COLOR = "#ef4444"


class UserVaultView:
    """Ventana principal con la interfaz de gestion de twiApliRoberto."""

    def __init__(self, root: tk.Tk, application: TwitterApplication) -> None:
        self.root = root
        self.application = application
        self.root.title("UserVault - CRUD Manager")
        self.root.geometry("820x540")
        self.root.minsize(760, 500)
        self.root.configure(bg=MAIN_BG)

        self._build_layout()
        self._load_users()

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)
        account_menu = tk.Menu(menu_bar, tearoff=False)
        account_menu.add_command(label="Cambiar contrasena", command=self._change_password)
        account_menu.add_command(label="Eliminar mi cuenta", command=self._delete_own_account)
        account_menu.add_separator()
        account_menu.add_command(label="Cerrar sesion", command=self._logout)
        account_menu.add_command(label="Salir", command=self.root.destroy)
        menu_bar.add_cascade(label="Ajustes de Cuenta", menu=account_menu)
        self.root.config(menu=menu_bar)

    def _build_layout(self) -> None:
        sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=155)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(
            sidebar,
            text="UserVault",
            bg=SIDEBAR_BG,
            fg="white",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=20)
        tk.Label(
            sidebar,
            text="Usuarios",
            bg=SIDEBAR_BG,
            fg="#94a3b8",
            anchor="w",
        ).pack(fill="x", padx=22, pady=5)
        tk.Label(
            sidebar,
            text="Configuración",
            bg=SIDEBAR_BG,
            fg="#94a3b8",
            anchor="w",
        ).pack(fill="x", padx=22, pady=5)
        self.status_label = tk.Label(
            sidebar,
            text="Estado:\nDesconectado",
            bg=SIDEBAR_BG,
            fg="#64748b",
            font=("Segoe UI", 9, "italic"),
            justify="left",
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=22, pady=15)

        self.main = tk.Frame(self.root, bg=MAIN_BG)
        self.main.pack(side="left", fill="both", expand=True, padx=22, pady=20)
        tk.Label(
            self.main,
            text="Gestión de Usuarios",
            bg=MAIN_BG,
            fg=TEXT_COLOR,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")

        actions = tk.Frame(self.main, bg=MAIN_BG)
        actions.pack(fill="x", pady=18)
        tk.Label(actions, text="Buscar:", bg=MAIN_BG, fg=TEXT_COLOR).pack(side="left")
        self.search_entry = tk.Entry(actions, width=22)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda _event: self._load_users())
        tk.Button(actions, text="Buscar", bd=1, padx=8, pady=2, command=self._load_users).pack(
            side="left", padx=(0, 10)
        )
        tk.Button(
            actions,
            text="Mostrar todos",
            bd=1,
            padx=8,
            pady=2,
            command=self._show_all_users,
        ).pack(side="left")
        tk.Button(
            actions,
            text="+ Nuevo Usuario",
            bg=PRIMARY_COLOR,
            fg="white",
            bd=0,
            padx=12,
            pady=6,
            font=("Segoe UI", 9, "bold"),
            command=self._new_user_dialog,
        ).pack(side="right")

        table_frame = ttk.Frame(self.main)
        table_frame.pack(fill="both", expand=True)
        self.users_table = ttk.Treeview(
            table_frame,
            columns=("id", "username", "password", "bio"),
            show="headings",
            selectmode="extended",
        )
        self.users_table.bind("<Button-1>", self._toggle_user_selection)
        for column, title in (
            ("id", "ID"),
            ("username", "Usuario"),
            ("password", "Contraseña"),
            ("bio", "Biografía"),
        ):
            self.users_table.heading(column, text=title)
        self.users_table.column("id", width=45, anchor="center")
        self.users_table.column("username", width=160)
        self.users_table.column("password", width=120)
        self.users_table.column("bio", width=220)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.users_table.yview)
        self.users_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.users_table.pack(fill="both", expand=True)

        buttons = tk.Frame(self.main, bg=MAIN_BG)
        buttons.pack(fill="x", pady=15)
        tk.Button(
            buttons,
            text="Editar seleccionado",
            bd=1,
            padx=10,
            pady=5,
            height=2,
            command=self._edit_selected_user,
        ).pack(side="left", padx=3)
        tk.Button(
            buttons,
            text="Eliminar",
            bg=DANGER_COLOR,
            fg="white",
            bd=0,
            padx=12,
            pady=6,
            command=self._delete_selected_users,
        ).pack(side="left", padx=3)

    def _toggle_user_selection(self, event: tk.Event) -> str | None:
        """Alterna una fila con un clic para facilitar la seleccion multiple."""
        item = self.users_table.identify_row(event.y)
        if not item:
            return None
        if item in self.users_table.selection():
            self.users_table.selection_remove(item)
        else:
            self.users_table.selection_add(item)
        return "break"

    def _load_users(self) -> None:
        for item in self.users_table.get_children():
            self.users_table.delete(item)
        search = self.search_entry.get().strip().lower()
        for user in self.application.users():
            if search and search not in user.username.lower():
                continue
            self.users_table.insert(
                "",
                "end",
                values=(user.id, user.username, user.password, user.bio),
            )

    def _show_all_users(self) -> None:
        self.search_entry.delete(0, tk.END)
        self._load_users()

    def _login_selected_user(self) -> None:
        selected = self.users_table.selection()
        if not selected:
            messagebox.showwarning("Atencion", "Selecciona un usuario de la tabla.")
            return
        values = self.users_table.item(selected[0], "values")
        try:
            user = self.application.login(values[1], values[2])
        except TwitterError as error:
            messagebox.showerror("Error", str(error))
            return
        self.status_label.config(text=f"Conectado:\n@{user.username}", fg="#22c55e")
        messagebox.showinfo("Login", f"Sesion iniciada como @{user.username}.")

    def _logout(self) -> None:
        if not self.application.is_logged_in:
            messagebox.showwarning("Atencion", "No hay ninguna sesion activa.")
            return
        self.application.logout()
        self.status_label.config(text="Estado:\nDesconectado", fg="#64748b")
        messagebox.showinfo("Sesion", "Sesion cerrada correctamente.")

    def _new_user_dialog(self) -> None:
        self._user_dialog("nuevo", None)

    def _edit_selected_user(self) -> None:
        selected = self.users_table.selection()
        if not selected:
            messagebox.showwarning("Atencion", "Selecciona un usuario de la lista.")
            return
        values = self.users_table.item(selected[0], "values")
        self._user_dialog("editar", values)

    def _user_dialog(self, mode: str, values: tuple[str, ...] | None) -> None:
        window = tk.Toplevel(self.root)
        editing = mode == "editar"
        window.title("Editar usuario" if editing else "Insertar usuario")
        window.geometry("380x360")
        window.resizable(False, False)
        window.configure(bg=MAIN_BG)
        window.transient(self.root)
        window.grab_set()

        pad = {"padx": 15, "pady": 5}
        tk.Label(
            window,
            text="Editar usuario" if editing else "Insertar usuario",
            font=("Segoe UI", 14, "bold"),
            bg=MAIN_BG,
            fg=TEXT_COLOR,
        ).pack(pady=10)

        tk.Label(window, text="Nombre de usuario:", bg=MAIN_BG, anchor="w").pack(
            fill="x", **pad
        )
        username_entry = tk.Entry(window, width=35)
        username_entry.insert(0, values[1] if editing and values else "")
        username_entry.pack(**pad)

        tk.Label(window, text="Contrasena:", bg=MAIN_BG, anchor="w").pack(
            fill="x", **pad
        )
        password_entry = tk.Entry(window, width=35, show="*")
        password_entry.insert(0, values[2] if editing and values else "")
        password_entry.pack(**pad)

        tk.Label(window, text="Biografia:", bg=MAIN_BG, anchor="w").pack(
            fill="x", **pad
        )
        bio_text = tk.Text(window, width=35, height=4)
        bio_text.insert("1.0", values[3] if editing and values else "")
        bio_text.pack(**pad)

        def save_user() -> None:
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            bio = bio_text.get("1.0", "end-1c").strip()
            if not username or not password:
                messagebox.showerror(
                    "Error",
                    "El usuario y la contrasena no pueden estar vacios.",
                    parent=window,
                )
                return
            try:
                if editing and values is not None:
                    self.application.update_user(int(values[0]), username, password, bio)
                else:
                    self.application.register(username, password, bio)
            except TwitterError as error:
                messagebox.showerror("Error", str(error), parent=window)
                return
            window.destroy()
            self._load_users()
            messagebox.showinfo("Exito", "Operacion realizada correctamente.", parent=self.root)

        button_frame = tk.Frame(window, bg=MAIN_BG)
        button_frame.pack(pady=15)
        tk.Button(
            button_frame,
            text="Guardar",
            bg=PRIMARY_COLOR,
            fg="white",
            bd=0,
            padx=12,
            pady=5,
            command=save_user,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="Cancelar",
            command=window.destroy,
            padx=10,
            pady=5,
        ).pack(side="left", padx=5)
        username_entry.focus_set()

    def _delete_selected_users(self) -> None:
        selected = self.users_table.selection()
        if not selected:
            messagebox.showwarning(
                "Atencion",
                "Selecciona al menos un usuario para eliminar.",
                parent=self.root,
            )
            return
        selected_users = [self.users_table.item(item, "values") for item in selected]
        user_ids = [int(values[0]) for values in selected_users]
        user_lines = "\n".join(f"ID {values[0]}: {values[1]}" for values in selected_users)
        quantity = len(user_ids)
        message = (
            f"¿Eliminar a estos {quantity} usuarios y todos sus tweets?\n\n"
            f"{user_lines}\n\nEsta accion no se puede deshacer."
        )
        if not messagebox.askyesno("Confirmar eliminacion", message, parent=self.root):
            return
        try:
            self.application.remove_users(user_ids)
        except TwitterError as error:
            messagebox.showerror("Error", str(error), parent=self.root)
            return
        if not self.application.is_logged_in:
            self.status_label.config(text="Estado:\nDesconectado", fg="#64748b")
        self._load_users()
        messagebox.showinfo(
            "Exito",
            f"Se eliminaron {quantity} usuario(s) y sus publicaciones.",
            parent=self.root,
        )

    def _change_password(self) -> None:
        if not self.application.is_logged_in:
            messagebox.showwarning("Atencion", "Inicia sesion primero.")
            return
        new_password = simpledialog.askstring(
            "Cambiar contrasena", "Introduce tu nueva contrasena:", show="*"
        )
        if new_password is None:
            return
        try:
            self.application.change_password(new_password)
        except TwitterError as error:
            messagebox.showerror("Error", str(error))
            return
        self._load_users()
        messagebox.showinfo("Exito", "Contrasena actualizada correctamente.")

    def _delete_own_account(self) -> None:
        if not self.application.is_logged_in:
            messagebox.showwarning("Atencion", "Inicia sesion primero.")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que quieres eliminar tu cuenta activa?"):
            return
        self.application.delete_account()
        self.status_label.config(text="Estado:\nDesconectado", fg="#64748b")
        self._load_users()
        messagebox.showinfo("Cuenta eliminada", "Tu cuenta se ha borrado correctamente.")


def main() -> None:
    create_db()
    root = tk.Tk()
    view = UserVaultView(root, TwitterApplication())
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()


if __name__ == "__main__":
    main()