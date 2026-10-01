"""Interfaz grafica Tkinter para gestionar la biblioteca."""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

try:
	from .libro import LibroCRUD
except ImportError:
	from libro import LibroCRUD


class BibliotecaApp:
	"""Ventana principal para las operaciones CRUD de libros."""

	def __init__(self, root: tk.Tk):
		self.root = root
		self.root.title("Biblioteca")
		self.root.geometry("1100x700")

		self.crud = LibroCRUD()
		self.crud.conectar()
		self.generos: dict[str, int] = {}

		self.titulo = tk.StringVar()
		self.autor = tk.StringVar()
		self.genero = tk.StringVar()
		self.anio = tk.StringVar()
		self.paginas = tk.StringVar()
		self.valoracion = tk.DoubleVar(value=0.0)
		self.estado = tk.StringVar(value="Pendiente")
		self.favorito = tk.BooleanVar(value=False)
		self.busqueda = tk.StringVar()
		self._columna_ordenada = None
		self._orden_inverso = False

		self._configurar_estilos()
		self._crear_widgets()
		self._cargar_generos()
		self.mostrar_todos()
		self.root.protocol("WM_DELETE_WINDOW", self._cerrar)

	def _configurar_estilos(self) -> None:
		estilo = ttk.Style(self.root)
		estilo.theme_use("clam")
		self.root.configure(bg="#17212b")

		estilo.configure("TFrame", background="#17212b")
		estilo.configure("TLabelframe", background="#22313f", bordercolor="#3a5368")
		estilo.configure(
			"TLabelframe.Label",
			background="#22313f",
			foreground="#8ee3d2",
			font=("Segoe UI", 10, "bold"),
		)
		estilo.configure(
			"TLabel",
			background="#22313f",
			foreground="#eef5f4",
			font=("Segoe UI", 9),
		)
		estilo.configure(
			"TButton",
			background="#2c9c91",
			foreground="#ffffff",
			borderwidth=0,
			padding=(12, 6),
			font=("Segoe UI", 9, "bold"),
		)
		estilo.map(
			"TButton",
			background=[("active", "#42b9aa"), ("pressed", "#217b73")],
		)
		estilo.configure(
			"Treeview",
			background="#f4f8f7",
			fieldbackground="#f4f8f7",
			foreground="#203039",
			rowheight=28,
			font=("Segoe UI", 9),
		)
		estilo.configure(
			"Treeview.Heading",
			background="#2b5368",
			foreground="#ffffff",
			padding=6,
			font=("Segoe UI", 9, "bold"),
		)
		estilo.map(
			"Treeview",
			background=[("selected", "#8ee3d2")],
			foreground=[("selected", "#17212b")],
		)

	def _crear_widgets(self) -> None:
		formulario = ttk.LabelFrame(self.root, text="Datos del libro", padding=10)
		formulario.pack(fill="x", padx=10, pady=10)

		ttk.Label(formulario, text="Titulo").grid(row=0, column=0, sticky="w")
		ttk.Entry(formulario, textvariable=self.titulo, width=32).grid(
			row=0, column=1, padx=5, pady=3
		)
		ttk.Label(formulario, text="Autor").grid(row=0, column=2, sticky="w")
		ttk.Entry(formulario, textvariable=self.autor, width=32).grid(
			row=0, column=3, padx=5, pady=3
		)

		ttk.Label(formulario, text="Genero").grid(row=1, column=0, sticky="w")
		self.genero_combo = ttk.Combobox(
			formulario, textvariable=self.genero, state="readonly", width=29
		)
		self.genero_combo.grid(row=1, column=1, padx=5, pady=3)
		ttk.Label(formulario, text="Año").grid(row=1, column=2, sticky="w")
		ttk.Entry(formulario, textvariable=self.anio, width=32).grid(
			row=1, column=3, padx=5, pady=3
		)

		ttk.Label(formulario, text="Paginas").grid(row=2, column=0, sticky="w")
		ttk.Entry(formulario, textvariable=self.paginas, width=32).grid(
			row=2, column=1, padx=5, pady=3
		)
		ttk.Label(formulario, text="Valoracion").grid(row=2, column=2, sticky="w")
		ttk.Scale(
			formulario, from_=0, to=10, variable=self.valoracion, orient="horizontal"
		).grid(row=2, column=3, sticky="ew", padx=5)

		ttk.Label(formulario, text="Estado").grid(row=3, column=0, sticky="w")
		estados = ttk.Frame(formulario)
		estados.grid(row=3, column=1, columnspan=3, sticky="w")
		for valor in ("Pendiente", "Leyendo", "Terminado"):
			ttk.Radiobutton(
				estados, text=valor, value=valor, variable=self.estado
			).pack(side="left", padx=(0, 10))
		ttk.Checkbutton(
			formulario, text="Favorito", variable=self.favorito
		).grid(row=4, column=0, sticky="w", pady=3)
		ttk.Label(formulario, text="Notas").grid(row=4, column=2, sticky="nw")
		self.notas = tk.Text(formulario, width=32, height=3)
		self.notas.grid(row=4, column=3, padx=5, pady=3)

		acciones = ttk.Frame(formulario)
		acciones.grid(row=5, column=0, columnspan=4, pady=(8, 0))
		ttk.Button(acciones, text="Guardar", command=self.guardar).pack(
			side="left", padx=3
		)
		ttk.Button(acciones, text="Modificar", command=self.modificar).pack(
			side="left", padx=3
		)
		ttk.Button(acciones, text="Eliminar", command=self.eliminar).pack(
			side="left", padx=3
		)
		ttk.Button(acciones, text="Limpiar", command=self.limpiar).pack(
			side="left", padx=3
		)

		busqueda = ttk.LabelFrame(self.root, text="Busqueda", padding=8)
		busqueda.pack(fill="x", padx=10, pady=(0, 8))
		ttk.Entry(busqueda, textvariable=self.busqueda, width=45).pack(
			side="left", padx=(0, 5)
		)
		ttk.Button(busqueda, text="Buscar", command=self.buscar).pack(side="left")
		ttk.Button(busqueda, text="Mostrar todos", command=self.mostrar_todos).pack(
			side="left", padx=5
		)

		listado = ttk.LabelFrame(self.root, text="Libros", padding=8)
		listado.pack(fill="both", expand=True, padx=10, pady=(0, 10))
		columnas = (
			"id", "titulo", "autor", "genero", "anio", "paginas",
			"valoracion", "estado", "favorito",
		)
		self.tabla = ttk.Treeview(
			listado, columns=columnas, show="headings", selectmode="extended"
		)
		encabezados = {
			"id": "ID", "titulo": "Titulo", "autor": "Autor",
			"genero": "Genero", "anio": "Año", "paginas": "Paginas",
			"valoracion": "Valoracion", "estado": "Estado", "favorito": "Favorito",
		}
		anchos = {"id": 45, "titulo": 180, "autor": 170, "genero": 110,
				  "anio": 65, "paginas": 70, "valoracion": 80, "estado": 100,
				  "favorito": 65}
		for columna in columnas:
			self.tabla.heading(
				columna,
				text=encabezados[columna],
				command=lambda nombre=columna: self.ordenar_por(nombre),
			)
			self.tabla.column(columna, width=anchos[columna], anchor="center")
		self.tabla.bind("<Button-1>", self._al_hacer_click)
		self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_libro)
		barra_vertical = ttk.Scrollbar(
			listado, orient="vertical", command=self.tabla.yview
		)
		self.tabla.configure(yscrollcommand=barra_vertical.set)
		self.tabla.pack(side="left", fill="both", expand=True)
		barra_vertical.pack(side="right", fill="y")

	def _cargar_generos(self) -> None:
		filas = self.crud.obtener_conexion().execute(
			"SELECT id, nombre FROM generos ORDER BY nombre"
		).fetchall()
		self.generos = {fila["nombre"]: fila["id"] for fila in filas}
		self.genero_combo["values"] = list(self.generos)

	def _datos_formulario(self) -> dict:
		if not self.titulo.get().strip():
			raise ValueError("El titulo es obligatorio")
		try:
			paginas = int(self.paginas.get())
		except ValueError as error:
			raise ValueError("Las paginas deben ser un numero entero") from error
		if paginas <= 50:
			raise ValueError("Las paginas deben ser mayores que 50")

		anio = int(self.anio.get()) if self.anio.get().strip() else None
		return {
			"titulo": self.titulo.get().strip(),
			"autor": self.autor.get().strip() or None,
			"genero_id": self.generos.get(self.genero.get()),
			"anio": anio,
			"paginas": paginas,
			"valoracion": round(self.valoracion.get(), 1),
			"estado": self.estado.get(),
			"favorito": int(self.favorito.get()),
			"notas": self.notas.get("1.0", "end").strip() or None,
		}

	def guardar(self) -> None:
		try:
			libro_id = self.crud.crear_libro(**self._datos_formulario())
			self.mostrar_todos()
			self.limpiar()
			messagebox.showinfo("Biblioteca", f"Libro guardado con ID {libro_id}")
		except (ValueError, sqlite3.IntegrityError) as error:
			messagebox.showerror("Error", str(error))

	def modificar(self) -> None:
		seleccionado = self.tabla.selection()
		if len(seleccionado) != 1:
			messagebox.showwarning("Biblioteca", "Selecciona un solo libro")
			return
		try:
			actualizado = self.crud.actualizar_libro(
				int(seleccionado[0]), **self._datos_formulario()
			)
			self.mostrar_todos()
			messagebox.showinfo("Biblioteca", "Libro actualizado" if actualizado else "No encontrado")
		except (ValueError, sqlite3.IntegrityError) as error:
			messagebox.showerror("Error", str(error))

	def eliminar(self) -> None:
		seleccionados = self.tabla.selection()
		if not seleccionados:
			messagebox.showwarning("Biblioteca", "Selecciona al menos un libro")
			return
		if not messagebox.askyesno("Confirmar", "¿Eliminar los libros seleccionados?"):
			return
		ids = [int(item) for item in seleccionados]
		self.crud.eliminar_libro(*ids)
		self.mostrar_todos()
		self.limpiar()

	def seleccionar_libro(self, _event=None) -> None:
		seleccionados = self.tabla.selection()
		if len(seleccionados) != 1:
			return
		libro = self.crud.obtener_libro_por_id(int(seleccionados[0]))
		if libro is None:
			return
		self.titulo.set(libro["titulo"])
		self.autor.set(libro["autor"] or "")
		self.genero.set(libro["genero_nombre"] or "")
		self.anio.set(str(libro["anio"] or ""))
		self.paginas.set(str(libro["paginas"]))
		self.valoracion.set(libro["valoracion"] or 0.0)
		self.estado.set(libro["estado"])
		self.favorito.set(bool(libro["favorito"]))
		self.notas.delete("1.0", "end")
		self.notas.insert("1.0", libro["notas"] or "")

	def _al_hacer_click(self, evento) -> None:
		"""Identifica la fila y la columna pulsadas en el Treeview."""
		columna_id = self.tabla.identify_column(evento.x)
		if not columna_id or columna_id == "#0":
			return

		indice = int(columna_id[1:]) - 1
		nombre_columna = self.tabla["columns"][indice]
		if self.tabla.identify_region(evento.x, evento.y) == "heading":
			messagebox.showinfo(
				"Cabecera",
				f"Has hecho clic en la cabecera:\n"
				f"'{nombre_columna}' (Columna {indice + 1})",
			)
			return

		fila_id = self.tabla.identify_row(evento.y)
		if not fila_id:
			return

		print(f"Clic en columna '{nombre_columna}', libro ID {fila_id}")

	def _mostrar_filas(self, libros: list[dict]) -> None:
		for item in self.tabla.get_children():
			self.tabla.delete(item)
		for libro in libros:
			self.tabla.insert(
				"", "end", iid=str(libro["id"]), values=(
					libro["id"], libro["titulo"], libro["autor"] or "",
					libro["genero_nombre"] or "", libro["anio"] or "",
					libro["paginas"], libro["valoracion"] or 0,
					libro["estado"], "Si" if libro["favorito"] else "No",
				)
			)

	def cargar_datos(self, libros: list[dict]) -> None:
		"""Limpia el Treeview e inserta una nueva lista de libros."""
		self._mostrar_filas(libros)

	def mostrar_todos(self) -> None:
		self.cargar_datos(self.crud.obtener_todos_los_libros())

	def ordenar_por(self, columna: str) -> None:
		"""Ordena la tabla al pulsar uno de sus encabezados."""
		if self._columna_ordenada == columna:
			self._orden_inverso = not self._orden_inverso
		else:
			self._columna_ordenada = columna
			self._orden_inverso = False

		self.cargar_datos(
			self.crud.obtener_todos_los_libros(
				ordenar_por=columna,
				descendente=self._orden_inverso,
			)
		)

	def buscar(self) -> None:
		texto = self.busqueda.get().strip().lower()
		libros = self.crud.obtener_todos_los_libros()
		if texto:
			libros = [
				libro for libro in libros
				if texto in (libro["titulo"] or "").lower()
				or texto in (libro["autor"] or "").lower()
			]
		self.cargar_datos(libros)

	def limpiar(self) -> None:
		self.titulo.set("")
		self.autor.set("")
		self.genero.set("")
		self.anio.set("")
		self.paginas.set("")
		self.valoracion.set(0.0)
		self.estado.set("Pendiente")
		self.favorito.set(False)
		self.notas.delete("1.0", "end")
		self.tabla.selection_remove(self.tabla.selection())

	def _cerrar(self) -> None:
		self.crud.cerrar_conexion()
		self.root.destroy()