import tkinter as tk

class Aplicacion:
    def __init__(self):
        self.ventana1 = tk.Tk()
        self.ventana1.title("Navegadores seleccionados:")
        self.navegadores = ["Chrome", "Safari", "Mozilla", "Brave"]
        self.variables = []
        self.controles = []

        for i in range(len(self.navegadores)):
            var = tk.IntVar()
            self.variables.append(var)
            check = tk.Checkbutton(
                self.ventana1,
                text=self.navegadores[i],
                variable=var,
                command=self.cambiar_titulo
            )
            check.grid(column=0, row=i, sticky="w", padx=10, pady=2)
            self.controles.append(check)

        self.ventana1.mainloop()

    def cambiar_titulo(self):
        texto_titulo = "Seleccionados: "
        for i in range(len(self.variables)):
            if self.variables[i].get() == 1:
                texto_titulo += self.navegadores[i] + " " 

            self.ventana1.title(texto_titulo)

aplicacion1 = Aplicacion()


    