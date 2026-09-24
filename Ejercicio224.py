import tkinter as tk


class Aplicacion:

    def __init__(self):
        self.ventana1 = tk.Tk()
        self.color = tk.StringVar(value="red")
        self.ventana1.configure(bg="red")

        for c, t in [("red", "Rojo"), ("green", "Verde"), ("blue", "Azul")]:
            tk.Radiobutton(
                self.ventana1,
                text=t,
                variable=self.color,
                value=c,
                command=self.cambiar,
            ).pack()

        self.ventana1.mainloop()

    def cambiar(self):
        self.ventana1.configure(bg=self.color.get())


app = Aplicacion()