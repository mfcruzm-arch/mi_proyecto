import tkinter as tk

class Aplicacion:
    def __init__(self):
        self.ventana1 = tk.Tk()
        self.ventana1.title("Redimensionar")

        # 1. Menú superior exactamente como lo hizo Roberto
        menubar1 = tk.Menu(self.ventana1)
        self.ventana1.config(menu=menubar1)

        opciones1 = tk.Menu(menubar1, tearoff=0)
        opciones1.add_command(label="Cambiar tamaño", command=self.redimensionar)
        menubar1.add_cascade(label="Cambiar tamaño", menu=opciones1)

        opciones2 = tk.Menu(menubar1, tearoff=0)
        opciones2.add_command(label="Salir", command=self.ventana1.quit)
        menubar1.add_cascade(label="Salir", menu=opciones2)

        # 2. Entradas para solicitar los valores de Ancho y Alto
        self.label1 = tk.Label(self.ventana1, text="Ingrese ancho:")
        self.label1.grid(column=0, row=0, padx=10, pady=5)
        self.entry1 = tk.Entry(self.ventana1)
        self.entry1.grid(column=1, row=0, padx=10, pady=5)

        self.label2 = tk.Label(self.ventana1, text="Ingrese alto:")
        self.label2.grid(column=0, row=1, padx=10, pady=5)
        self.entry2 = tk.Entry(self.ventana1)
        self.entry2.grid(column=1, row=1, padx=10, pady=5)

        self.ventana1.mainloop()

    def redimensionar(self):
        # Tomamos el texto de las entradas en lugar de valores fijos
        ancho = self.entry1.get()
        alto = self.entry2.get()

        if ancho and alto:
            self.ventana1.geometry(f"{ancho}x{alto}")

aplicacion1 = Aplicacion()