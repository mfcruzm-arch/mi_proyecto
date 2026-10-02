import tkinter as tk

try:
    from .interfaz import BibliotecaApp
except ImportError:
    from interfaz import BibliotecaApp


if __name__ == "__main__":
	ventana = tk.Tk()
	BibliotecaApp(ventana)
	ventana.mainloop()
