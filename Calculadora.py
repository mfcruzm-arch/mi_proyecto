import tkinter as tk
from tkinter import ttk

class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.title("Calculadora KASIO")
        self.geometry("320x410")
        self.resizable(False, False)

        # Configurar las 4 columnas para que se expandan proporcionalmente
        for i in range(4):
            self.columnconfigure(i, weight=1)
        
        # Configurar las filas de los botones para que se ajusten verticalmente
        for i in range(3, 7):
            self.rowconfigure(i, weight=1)

        # 1. Pantalla de la calculadora (Fila 0)
        self.pantalla = ttk.Entry(self, font=("Arial", 18), justify="right")
        self.pantalla.grid(row=0, column=0, columnspan=4, padx=10, pady=(15, 5), sticky="ew")

        # 2. Marca KASIO justo debajo de la pantalla, alineada a la izquierda (Fila 1)
        self.marca = ttk.Label(self, text="KASIO", font=("Arial", 9, "bold"))
        self.marca.grid(row=1, column=0, columnspan=2, padx=12, pady=(2, 8), sticky="w")

        # Lista de botones y sus posiciones (filas desplazadas a partir de la fila 3)
        botones = [
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
            ('0', 6, 0), ('C', 6, 1), ('=', 6, 2), ('+', 6, 3)
        ]

        # 3. Crear botones ajustados a la cuadrícula
        for (texto, fila, columna) in botones:
            btn = ttk.Button(
                self, 
                text=texto, 
                command=lambda t=texto: self.al_pulsar_boton(t)
            )
            btn.grid(row=fila, column=columna, padx=3, pady=3, sticky="nsew")

    def al_pulsar_boton(self, valor):
        if valor == 'C':
            self.pantalla.delete(0, tk.END)
        elif valor == '=':
            try:
                resultado = eval(self.pantalla.get())
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, str(resultado))
            except Exception:
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, "Error")
        else:
            self.pantalla.insert(tk.END, valor)

if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()