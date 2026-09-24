import tkinter as tk


class CalculadoraKasio:


  def __init__(self, root):

    # ---------------------------------------------------------

    # 1. CONFIGURACIÓN GENERAL DE LA VENTANA PRINCIPAL

    # ---------------------------------------------------------

    self.root = root

    self.root.title("KASIO")  # Título de la ventana

    self.root.geometry("320x460")  # Tamaño en píxeles (ancho x alto)

    self.root.resizable(False, False)  # Desactiva el redimensionamiento

    self.root.configure(bg="#e6e6e6")  # Color de fondo gris claro


    # ---------------------------------------------------------

    # 2. PANTALLA / DISPLAY DE LA CALCULADORA

    # ---------------------------------------------------------

    # Creamos una entrada de texto (Entry) para mostrar los números ingresados

    self.pantalla = tk.Entry(

        root,

        font=("Consolas", 20, "bold"),  # Fuente estilo calculadora digital

        justify="right",  # Alineación del texto a la derecha

        bd=5,  # Ancho del borde

        relief=tk.SUNKEN,  # Efecto visual de hundido/insertado

        bg="#c3d9c3",  # Color de fondo verde pastel (estilo LCD clásico)

        fg="#000000",  # Color del texto (negro)

    )


    # Posicionamos la pantalla en la celda (Fila 0, Columna 0) expandiéndose a 4 columnas

    self.pantalla.grid(

        row=0, column=0, columnspan=4, padx=15, pady=(15, 10), sticky="nsew"

    )


    # ---------------------------------------------------------

    # 3. MARCA / TEXTO "KASIO"

    # ---------------------------------------------------------

    # Texto decorativo en lugar de un botón, respetando el dibujo

    self.label_kasio = tk.Label(

        root,

        text="KASIO",

        font=("Arial", 16, "bold"),

        bg="#e6e6e6",

        fg="#333333",

        anchor="w",  # Alineado a la izquierda

    )

    # Ocupa las dos primeras columnas de la fila 1

    self.label_kasio.grid(

        row=1, column=0, columnspan=2, padx=15, pady=5, sticky="w"

    )


    # Fuente compartida para uniformidad en los botones

    btn_font = ("Arial", 14, "bold")


    # ---------------------------------------------------------

    # 4. BOTONES ESPECIALES DE LA PRIMERA FILA (C y =)

    # ---------------------------------------------------------

    # Botón para borrar/limpiar 'C'

    tk.Button(

        root,

        text="C",

        font=btn_font,

        bg="#ff6b6b",

        fg="white",

        command=self.limpiar,  # Al hacer clic ejecuta el método self.limpiar

    ).grid(row=1, column=2, padx=5, pady=5, sticky="nsew")


    # Botón para calcular el resultado '='

    tk.Button(

        root,

        text="=",

        font=btn_font,

        bg="#4ecdc4",

        fg="white",

        command=self.calcular,  # Al hacer clic ejecuta el método self.calcular

    ).grid(row=1, column=3, padx=5, pady=5, sticky="nsew")


    # ---------------------------------------------------------

    # 5. MATRIZ DE BOTONES NUMÉRICOS Y OPERADORES

    # ---------------------------------------------------------

    # Fila 2: 1, 2, 3, +

    self.crear_boton("1", 2, 0)

    self.crear_boton("2", 2, 1)

    self.crear_boton("3", 2, 2)

    self.crear_boton("+", 2, 3, bg="#f0a500", fg="white")


    # Fila 3: 4, 5, 6, -

    self.crear_boton("4", 3, 0)

    self.crear_boton("5", 3, 1)

    self.crear_boton("6", 3, 2)

    self.crear_boton("-", 3, 3, bg="#f0a500", fg="white")


    # Fila 4: 7, 8, 9, *

    self.crear_boton("7", 4, 0)

    self.crear_boton("8", 4, 1)

    self.crear_boton("9", 4, 2)

    self.crear_boton("*", 4, 3, bg="#f0a500", fg="white")


    # Fila 5: 0 y /

    self.crear_boton("0", 5, 1)  # El 0 está en la columna central (columna 1)

    self.crear_boton(

        "/", 5, 3, bg="#f0a500", fg="white"

    )  # La división '/' en la columna 3


    # ---------------------------------------------------------

    # 6. DISTRIBUCIÓN RECTANGULAR Y PROPORCIONES DE LA REJILLA

    # ---------------------------------------------------------

    # Asegura que las 4 columnas y las 6 filas crezcan proporcionalmente

    for i in range(4):

      root.grid_columnconfigure(i, weight=1)

    for i in range(6):

      root.grid_rowconfigure(i, weight=1)


  # -----------------------------------------------------------

  # MÉTODOS AUXILIARES DE LA INTERFAZ Y LÓGICA

  # -----------------------------------------------------------

  def crear_boton(

      self, texto, fila, columna, bg="#ffffff", fg="#000000", columnspan=1

  ):

    """Método reutilizable para crear y colocar un botón en la rejilla."""

    btn = tk.Button(

        self.root,

        text=texto,

        font=("Arial", 14, "bold"),

        bg=bg,

        fg=fg,

        # Se usa lambda para pasar el valor específico del botón al método self.pulsar

        command=lambda: self.pulsar(texto),

    )

    btn.grid(

        row=fila,

        column=columna,

        columnspan=columnspan,

        padx=5,

        pady=5,

        sticky="nsew",  # Expande el botón para llenar toda su celda

    )


  def pulsar(self, valor):

    """Inserta el caracter o número pulsado al final de la pantalla."""

    self.pantalla.insert(tk.END, valor)


  def limpiar(self):

    """Borra todo el contenido de la pantalla."""

    self.pantalla.delete(0, tk.END)


  def calcular(self):

    """Toma la expresión en la pantalla, la evalúa numéricamente y muestra el resultado."""

    try:

      expresion = self.pantalla.get()

      resultado = eval(expresion)  # Evalúa matemáticamente el texto

      self.pantalla.delete(0, tk.END)

      self.pantalla.insert(0, str(resultado))

    except Exception:

      # Si hay un error matemático (ej. dividir por cero), muestra 'Error'

      self.pantalla.delete(0, tk.END)

      self.pantalla.insert(0, "Error")



# -------------------------------------------------------------

# INICIALIZACIÓN DE LA APLICACIÓN

# -------------------------------------------------------------

if __name__ == "__main__":

  root = tk.Tk()  # Crea la ventana principal de Tkinter

  app = CalculadoraKasio(root)  # Instancia la clase de la calculadora

  root.mainloop()  # Inicia el bucle principal de eventos de la GUI