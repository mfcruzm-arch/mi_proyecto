import tkinter as tk


class Aplicacion:

  def __init__(self):
    self.FICHERO = r'C:\Users\manana\Desktop\mi_proyecto\paises.csv'

    self.ventana1 = tk.Tk()
    self.ventana1.title('paises')

    # 1. Etiqueta para el nombre (Columna 0, Fila 0)
    self.label_nombre = tk.Label(self.ventana1, text='Ingrese el nombre:')
    self.label_nombre.grid(column=0, row=0, padx=5, pady=10, sticky='e')

    # 2. Caja de texto para escribir el nombre AL LADO (Columna 1, Fila 0)
    self.entry_nombre = tk.Entry(self.ventana1)
    self.entry_nombre.grid(column=1, row=0, padx=5, pady=10, sticky='w')

    # Scrollbar a la derecha de la Listbox
    self.scroll1 = tk.Scrollbar(self.ventana1)
    self.scroll1.grid(column=2, row=1, sticky='NS')

    # Listbox abarcando las dos columnas (columnspan=2)
    self.listbox1 = tk.Listbox(
        self.ventana1, yscrollcommand=self.scroll1.set
    )
    self.listbox1.grid(column=0, row=1, columnspan=2, padx=10, pady=5)
    self.scroll1.configure(command=self.listbox1.yview)

    # Cargar los países desde el archivo
    self.generador_opciones(self.FICHERO)

    # Botón centrado en la fila inferior
    self.boton1 = tk.Button(
        self.ventana1, text='Recuperar', command=self.recuperar
    )
    self.boton1.grid(column=0, row=2, columnspan=2, pady=10)

    self.ventana1.mainloop()

  def generador_opciones(self, fichero):
    try:
      with open(fichero, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
          pais = line.strip().split(',')
          if pais[0]:
            self.listbox1.insert(i, pais[0])
    except FileNotFoundError:
      self.listbox1.insert(0, 'Archivo no encontrado')

  def recuperar(self):
    nombre = self.entry_nombre.get()

    if len(self.listbox1.curselection()) != 0:
      posicion = self.listbox1.curselection()[0]
      pais_seleccionado = self.listbox1.get(posicion)

      # Actualiza la barra de título con el nombre y país
      self.ventana1.title(f'{nombre} - {pais_seleccionado}')


aplicacion1 = Aplicacion()