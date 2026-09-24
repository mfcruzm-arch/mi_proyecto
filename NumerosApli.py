import tkinter as tk


class ContadorBotonesApp:

    def __init__(self, root):
        # ---------------------------------------------------------
        # 1. CONFIGURACIÓN GENERAL DE LA VENTANA PRINCIPAL
        # ---------------------------------------------------------
        self.root = root
        self.root.title("Historial de Botones")
        self.root.geometry("400x200")
        
        # PERMITIR REDIMENSIONAR: Se cambia a True en ancho y alto
        self.root.resizable(True, True)

        # Atributo privado para almacenar el historial
        self.__presionados = []

        # ---------------------------------------------------------
        # 2. CREACIÓN DE LOS BOTONES (1 AL 5)
        # ---------------------------------------------------------
        for i in range(1, 6):
            btn = tk.Button(
                root,
                text=str(i),
                font=("Arial", 12, "bold"),
                width=4,
                bg="#e6e6e6",
                command=lambda num=i: self.presionar_numero(num),
            )
            btn.grid(row=0, column=i - 1, padx=5, pady=20)

        # ---------------------------------------------------------
        # 3. ETIQUETA CON SALTO DE LÍNEA AUTOMÁTICO (WRAPLENGTH)
        # ---------------------------------------------------------
        self.label_resultado = tk.Label(
            root,
            text="Presionados: ",
            font=("Arial", 11, "bold"),
            fg="#333333",
            anchor="w",
            justify="left",
            wraplength=360  # Ajusta el texto al ancho en píxeles antes de hacer un salto de línea
        )
        self.label_resultado.grid(
            row=1, column=0, columnspan=5, padx=15, pady=10, sticky="ew"
        )

        # Asignación de pesos para que la rejilla se adapte al estirar la ventana
        for col in range(5):
            root.grid_columnconfigure(col, weight=1)
            
        # Detecta cuando cambias el tamaño de la ventana para recalcular el salto de línea
        self.root.bind("<Configure>", self._al_redimensionar)

    # ---------------------------------------------------------
    # MÉTODOS AUXILIARES Y LÓGICA
    # ---------------------------------------------------------
    def presionar_numero(self, numero):
        """Añade el número presionado a la lista y actualiza la pantalla."""
        self.__presionados.append(str(numero))
        historial_str = " ".join(self.__presionados)
        self.label_resultado.config(text=f"Presionados: {historial_str}")

    def _al_redimensionar(self, event):
        """Ajusta el ancho del salto de línea dinámicamente al estirar la ventana."""
        # Se restan los márgenes laterales (padx) para que no se corte el texto
        nuevo_ancho = self.root.winfo_width() - 30
        if nuevo_ancho > 100:
            self.label_resultado.config(wraplength=nuevo_ancho)


# -------------------------------------------------------------
# INICIALIZACIÓN DE LA APLICACIÓN
# -------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ContadorBotonesApp(root)
    root.mainloop()