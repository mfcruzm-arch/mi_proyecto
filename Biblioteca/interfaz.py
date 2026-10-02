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
		self.root.geometry("620x430")
		self.root.configure(bg="#dfe1e4")
		self.root.resizable(False, False)
		self.root.overrideredirect(True)
		self._drag_x = 0
		self._drag_y = 0

		self.crud = LibroCRUD()
		self.crud.conectar()
		self._columnas: list[str] = self.crud.obtener_columnas()
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
		self.notas: tk.Text | None = None
		self.genero_combo: ttk.Combobox | None = None
		self._ventana_formulario: tk.Toplevel | None = None
		self._orden_multi = []
		self._direcciones_orden = {}

		self._configurar_estilos()
		self._crear_widgets()
		self._cargar_generos()
		self.mostrar_todos()
		self.root.protocol("WM_DELETE_WINDOW", self._cerrar)

	def _configurar_estilos(self) -> None:
		estilo = ttk.Style(self.root)
		estilo.theme_use("clam")
		self.root.configure(bg="#dfe1e4")

		estilo.configure("TFrame", background="#dfe1e4")
		estilo.configure("TLabelframe", background="#dfe1e4", bordercolor="#c9c9c9")
		estilo.configure(
			"TLabelframe.Label",
			background="#dfe1e4",
			foreground="#2d2d2d",
			font=("Segoe UI", 10, "bold"),
		)
		estilo.configure(
			"TLabel",
			background="#dfe1e4",
			foreground="#333333",
			font=("Segoe UI", 9),
		)
		estilo.configure(
			"TButton",
			background="#dfe1e4",
			foreground="#444444",
			borderwidth=0,
			padding=(8, 4),
			font=("Segoe UI", 9),
		)
		estilo.map(
			"TButton",
			background=[("active", "#d5d8dc"), ("pressed", "#c7ccd1")],
		)
		estilo.configure(
			"Treeview",
			background="#ffffff",
			fieldbackground="#ffffff",
			foreground="#1e1e1e",
			rowheight=24,
			font=("Segoe UI", 9),
		)
		estilo.configure(
			"Treeview.Heading",
			background="#dfe8f2",
			foreground="#2a2d2f",
			padding=6,
			font=("Segoe UI", 9, "bold"),
		)
		estilo.map(
			"Treeview",
			background=[("selected", "#cfe3ff")],
			foreground=[("selected", "#111111")],
		)

	def _crear_widgets(self) -> None:
		barra_titulo = tk.Frame(self.root, bg="#d8d8d8", height=28)
		barra_titulo.pack(fill="x")
		barra_titulo.pack_propagate(False)
		barra_titulo.bind("<ButtonPress-1>", self._iniciar_arrastre)
		barra_titulo.bind("<B1-Motion>", self._mover_ventana)

		icono = tk.Label(barra_titulo, text="📘", bg="#d8d8d8", fg="#2f2f2f", font=("Segoe UI", 11, "bold"))
		icono.pack(side="left", padx=(10, 5), pady=2)
		titulo = tk.Label(barra_titulo, text="Biblioteca", bg="#d8d8d8", fg="#1e1e1e", font=("Segoe UI", 10, "bold"))
		titulo.pack(side="left", pady=2)
		titulo.bind("<ButtonPress-1>", self._iniciar_arrastre)
		titulo.bind("<B1-Motion>", self._mover_ventana)

		botones = tk.Frame(barra_titulo, bg="#d8d8d8")
		botones.pack(side="right", padx=(0, 8), pady=2)
		btn_min = tk.Button(botones, text="—", bg="#d8d8d8", bd=0, relief="flat", width=2, height=1, command=self.root.iconify)
		btn_min.pack(side="left")
		btn_cerrar = tk.Button(botones, text="✕", bg="#d8d8d8", bd=0, relief="flat", width=2, height=1, command=self.root.destroy)
		btn_cerrar.pack(side="left", padx=(6, 0))

		contenedor = tk.Frame(self.root, bg="#f0f0f0", padx=8, pady=8)
		contenedor.pack(fill="both", expand=True)
		zona_busqueda = ttk.Frame(contenedor)
		zona_busqueda.pack(fill="x", pady=(0, 8))
		ttk.Label(zona_busqueda, text="Buscar título o autor:").pack(
			side="left", padx=(0, 8)
		)
		self.entrada_busqueda = ttk.Entry(
			zona_busqueda,
			textvariable=self.busqueda,
		)
		self.entrada_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 6))
		self.entrada_busqueda.bind("<Return>", lambda _evento: self.buscar())
		ttk.Button(zona_busqueda, text="Buscar", command=self.buscar).pack(side="left")
		ttk.Button(
			zona_busqueda,
			text="Limpiar",
			command=self.limpiar_busqueda,
		).pack(side="left", padx=(4, 0))
		ttk.Button(
			zona_busqueda,
			text="Nuevo libro",
			command=self.abrir_formulario,
		).pack(side="left", padx=(6, 0))

		marco_tabla = tk.Frame(contenedor, bg="#f0f0f0")
		marco_tabla.pack(fill="both", expand=True)

		columnas = tuple(self._columnas)
		self.tabla = ttk.Treeview(
			marco_tabla,
			columns=columnas,
			show="headings",
			selectmode="browse",
			height=15,
			xscrollcommand=lambda *args: barra_horizontal.set(*args),
		)
		self._encabezados = {
			"id": "ID",
			"titulo": "Título",
			"autor": "Autor",
			"genero_id": "Género",
			"anio": "Año",
			"paginas": "Páginas",
			"valoracion": "Valoración",
			"estado": "Estado",
			"favorito": "Favorito",
			"notas": "Notas",
		}
		for nombre in columnas:
			self.tabla.heading(
				nombre,
				text=self._encabezados.get(nombre, nombre),
				command=lambda col=nombre: self._mostrar_nombre_columna(col),
			)
		anchos = {
			"id": 55,
			"titulo": 180,
			"autor": 160,
			"genero_id": 130,
			"anio": 70,
			"paginas": 75,
			"valoracion": 95,
			"estado": 100,
			"favorito": 80,
			"notas": 200,
		}
		for nombre, ancho in anchos.items():
			self.tabla.column(
				nombre,
				width=ancho,
				minwidth=45,
				stretch=False,
				anchor="center",
			)

		barra_horizontal = ttk.Scrollbar(
			marco_tabla,
			orient="horizontal",
			command=self.tabla.xview,
		)
		marco_tabla.rowconfigure(0, weight=1)
		marco_tabla.columnconfigure(0, weight=1)
		self.tabla.grid(row=0, column=0, sticky="nsew")
		barra_horizontal.grid(row=1, column=0, sticky="ew")

		self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_libro)
		self.tabla.bind("<Shift-Button-1>", self._ordenar_multinivel)

		self.tabla.tag_configure("selected", background="#dfe8f2")

		self._orden_multi = []
		self._direcciones_orden = {}

	def _mostrar_nombre_columna(
		self,
		nombre_columna: str,
		agregar_criterio: bool = False,
	) -> None:
		messagebox.showinfo(
			title="Encabezado",
			message=f"Has hecho clic en: {nombre_columna}",
		)
		self.ordenar_por(nombre_columna, agregar_criterio=agregar_criterio)

	def _ordenar_multinivel(self, evento) -> str | None:
		if self.tabla.identify_region(evento.x, evento.y) != "heading":
			return None
		columna_id = self.tabla.identify_column(evento.x)
		indice = int(columna_id[1:]) - 1
		self._mostrar_nombre_columna(
			self._columnas[indice],
			agregar_criterio=True,
		)
		return "break"

	def _iniciar_arrastre(self, event):
		self._drag_x = event.x_root - self.root.winfo_rootx()
		self._drag_y = event.y_root - self.root.winfo_rooty()

	def _mover_ventana(self, event):
		nueva_x = event.x_root - self._drag_x
		nueva_y = event.y_root - self._drag_y
		self.root.geometry(f"+{nueva_x}+{nueva_y}")

	def _cargar_generos(self) -> None:
		filas = self.crud.obtener_conexion().execute(
			"SELECT id, nombre FROM generos ORDER BY nombre"
		).fetchall()
		self.generos = {fila["nombre"]: fila["id"] for fila in filas}
		if self.genero_combo is not None:
			self.genero_combo["values"] = list(self.generos)

	def abrir_formulario(self) -> None:
		if self._ventana_formulario is not None and self._ventana_formulario.winfo_exists():
			self._ventana_formulario.deiconify()
			self._ventana_formulario.lift()
			return

		ventana = tk.Toplevel(self.root)
		self._ventana_formulario = ventana
		ventana.title("Nuevo libro")
		ventana.geometry("460x610")
		ventana.minsize(420, 560)
		ventana.transient(self.root)

		contenido = ttk.Frame(ventana, padding=16)
		contenido.pack(fill="both", expand=True)
		contenido.columnconfigure(1, weight=1)

		campos = (
			("Título", self.titulo),
			("Autor", self.autor),
			("Año", self.anio),
			("Páginas", self.paginas),
		)
		for fila, (etiqueta, variable) in enumerate(campos):
			ttk.Label(contenido, text=etiqueta).grid(
				row=fila, column=0, sticky="w", padx=(0, 12), pady=6
			)
			ttk.Entry(contenido, textvariable=variable).grid(
				row=fila, column=1, sticky="ew", pady=6
			)

		ttk.Label(contenido, text="Género").grid(
			row=4, column=0, sticky="w", padx=(0, 12), pady=6
		)
		self.genero_combo = ttk.Combobox(
			contenido,
			textvariable=self.genero,
			state="readonly",
			values=list(self.generos),
		)
		self.genero_combo.grid(row=4, column=1, sticky="ew", pady=6)

		ttk.Label(contenido, text="Valoración").grid(
			row=5, column=0, sticky="w", padx=(0, 12), pady=6
		)
		tk.Scale(
			contenido,
			from_=0,
			to=10,
			variable=self.valoracion,
			orient="horizontal",
		).grid(row=5, column=1, sticky="ew", pady=6)

		ttk.Label(contenido, text="Estado").grid(
			row=6, column=0, sticky="nw", padx=(0, 12), pady=6
		)
		marco_estado = ttk.Frame(contenido)
		marco_estado.grid(row=6, column=1, sticky="w", pady=6)
		for estado in ("Pendiente", "Leyendo", "Terminado"):
			ttk.Radiobutton(
				marco_estado,
				text=estado,
				value=estado,
				variable=self.estado,
			).pack(anchor="w")

		ttk.Checkbutton(
			contenido,
			text="Marcar como favorito",
			variable=self.favorito,
		).grid(row=7, column=1, sticky="w", pady=6)

		ttk.Label(contenido, text="Notas").grid(
			row=8, column=0, sticky="nw", padx=(0, 12), pady=6
		)
		marco_notas = ttk.Frame(contenido)
		marco_notas.grid(row=8, column=1, sticky="nsew", pady=6)
		contenido.rowconfigure(8, weight=1)
		self.notas = tk.Text(marco_notas, height=6, wrap="word")
		barra_notas = ttk.Scrollbar(
			marco_notas,
			orient="vertical",
			command=self.notas.yview,
		)
		self.notas.configure(yscrollcommand=barra_notas.set)
		self.notas.pack(side="left", fill="both", expand=True)
		barra_notas.pack(side="right", fill="y")

		ttk.Button(
			contenido,
			text="Cerrar",
			command=lambda: self._cerrar_formulario(ventana),
		).grid(row=9, column=1, sticky="e", pady=(12, 0))
		ventana.protocol(
			"WM_DELETE_WINDOW",
			lambda: self._cerrar_formulario(ventana),
		)

	def _cerrar_formulario(self, ventana: tk.Toplevel) -> None:
		if self._ventana_formulario is ventana:
			self._ventana_formulario = None
			self.genero_combo = None
			self.notas = None
		ventana.destroy()

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
			"notas": (
				self.notas.get("1.0", "end").strip() or None
				if self.notas is not None else None
			),
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
		if self.notas is not None:
			self.notas.delete("1.0", "end")
			self.notas.insert("1.0", libro["notas"] or "")

	def _al_hacer_click(self, evento) -> None:
		"""Solo se usa para clics sobre filas; la ordenación va por cabecera."""
		columna_id = self.tabla.identify_column(evento.x)
		if not columna_id or columna_id == "#0":
			return

		indice = int(columna_id[1:]) - 1
		nombre_columna = self.tabla["columns"][indice]
		if self.tabla.identify_region(evento.x, evento.y) == "heading":
			return

		fila_id = self.tabla.identify_row(evento.y)
		if not fila_id:
			return

		print(f"Clic en columna '{nombre_columna}', libro ID {fila_id}")

	def _cargar_datos_demo(self) -> None:
		for item in self.tabla.get_children():
			self.tabla.delete(item)
		filas = [
			(1, "1984", "George Orwell", 3, 1),
			(19, "100 de años de soledad", "Gabriel García Márquez", 3, 1),
			(20, "Crónica de una muerte anunciada", "Gabriel García Márquez", 3, 1),
			(25, "100 de años de soledad", "Gabriel García Márquez", 3, 1),
			(26, "100 de años de soledad", "Gabriel García Márquez", 3, 1),
			(27, "100 de años de soledad", "Gabriel García Márquez", 3, 1),
			(28, "100 de años de soledad", "Gabriel García Márquez", 3, 1),
			(29, "100 de años de soledad", "Gabriel García Márquez", 3, 1),
			(30, "100 de años de soledad", "Gabriel García Márquez", 3, 1),
			(31, "100 de años de soledad", "Gabriel García Márquez", 3, 1),
		]
		for fila in filas:
			self.tabla.insert("", "end", values=fila)
		self.tabla.selection_set("1")
		self.tabla.focus("1")

	def _mostrar_filas(self, libros: list[dict]) -> None:
		for item in self.tabla.get_children():
			self.tabla.delete(item)
		for libro in libros:
			valores_libro = {
				**libro,
				"genero_id": libro["genero_nombre"] or "",
				"favorito": "Sí" if libro.get("favorito") else "No",
			}
			valores = tuple(
				"" if valores_libro.get(columna) is None else valores_libro[columna]
				for columna in self._columnas
			)
			self.tabla.insert(
				"", "end", iid=str(libro["id"]), values=valores
			)

	def cargar_datos(
		self,
		order_by: str | list[tuple[str, bool]] | None = None,
	) -> None:
		"""Consulta los libros y recarga el Treeview con el orden indicado."""
		libros = self.crud.obtener_todos_los_libros(ordenar_por=order_by)
		self._mostrar_filas(libros)

	def mostrar_todos(self) -> None:
		orden_por = [
			(col, self._direcciones_orden.get(col, False))
			for col in self._orden_multi
		]
		self.cargar_datos(order_by=orden_por or "id")

	def _actualizar_encabezados_orden(self) -> None:
		for columna, texto in self._encabezados.items():
			if columna in self._orden_multi:
				prioridad = self._orden_multi.index(columna) + 1
				flecha = "↓" if self._direcciones_orden[columna] else "↑"
				texto = f"{texto} {flecha}{prioridad}"
			self.tabla.heading(columna, text=texto)

	def ordenar_por(self, columna: str, agregar_criterio: bool = False) -> None:
		"""Activa o quita criterios de ordenación al pulsar las cabeceras."""
		if agregar_criterio:
			if columna in self._orden_multi:
				self._orden_multi.remove(columna)
				self._direcciones_orden.pop(columna, None)
			else:
				self._orden_multi.append(columna)
				self._direcciones_orden[columna] = False
		else:
			if self._orden_multi == [columna]:
				self._orden_multi = []
				self._direcciones_orden = {}
			else:
				self._orden_multi = [columna]
				self._direcciones_orden = {columna: False}

		self._actualizar_encabezados_orden()
		orden_por = [
			(col, self._direcciones_orden.get(col, False))
			for col in self._orden_multi
		]
		self.cargar_datos(order_by=orden_por or "id")

	def buscar(self) -> None:
		texto = self.busqueda.get().strip().lower()
		orden_por = [
			(col, self._direcciones_orden.get(col, False))
			for col in self._orden_multi
		]
		libros = self.crud.obtener_todos_los_libros(ordenar_por=orden_por or "id")
		if texto:
			libros = [
				libro for libro in libros
				if texto in (libro["titulo"] or "").lower()
				or texto in (libro["autor"] or "").lower()
			]
		self._mostrar_filas(libros)

	def limpiar_busqueda(self) -> None:
		self.busqueda.set("")
		self.mostrar_todos()

	def limpiar(self) -> None:
		self.titulo.set("")
		self.autor.set("")
		self.genero.set("")
		self.anio.set("")
		self.paginas.set("")
		self.valoracion.set(0.0)
		self.estado.set("Pendiente")
		self.favorito.set(False)
		if self.notas is not None:
			self.notas.delete("1.0", "end")
		self.tabla.selection_remove(self.tabla.selection())

	def _cerrar(self) -> None:
		self.crud.cerrar_conexion()
		self.root.destroy()