import tkinter as tk


class SeleccionGeneroApp:

    def __init__(self, root):
        # 1. CONFIGURACIÓN GENERAL DE LA VENTANA PRINCIPAL
        self.root = root
        self.root.title("Selecciona una opción")
        self.root.geometry("300x150")
        self.root.resizable(False, False)

        # Contenedor para centrar los botones
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        # 2. CREACIÓN DE LOS BOTONES
        # Usamos lambda para pasar la etiqueta correspondiente al presionar
        self.btn_varon = tk.Button(
            frame,
            text="varón",
            font=("Arial", 11, "bold"),
            bg="#4ecdc4",
            fg="white",
            width=10,
            command=lambda: self.cambiar_titulo("varón"),
        )
        self.btn_varon.pack(side=tk.LEFT, padx=10)

        self.btn_mujer = tk.Button(
            frame,
            text="mujer",
            font=("Arial", 11, "bold"),
            bg="#ff6b6b",
            fg="white",
            width=10,
            command=lambda: self.cambiar_titulo("mujer"),
        )
        self.btn_mujer.pack(side=tk.LEFT, padx=10)

    # 3. MÉTODOS AUXILIARES Y LÓGICA
    def cambiar_titulo(self, texto):
        """Modifica el título de la barra superior de la ventana."""
        self.root.title(texto)


# -------------------------------------------------------------
# INICIALIZACIÓN DE LA APLICACIÓN
# -------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SeleccionGeneroApp(root)
    root.mainloop()