# ApliTwiRob

Aplicacion de escritorio hecha con Python, Tkinter y SQLite para gestionar:

- cuentas de usuario;
- tweets de hasta 280 caracteres;
- retweets;
- timeline y eliminacion de tweets propios.
- borrado multiple de usuarios con confirmacion previa.

## Estructura VCM

- `modelo.py`: base de datos, usuarios, tweets y reglas de negocio.
- `aplicacion.py`: controlador y casos de uso de la aplicacion.
- `chat.py`: vista grafica UserVault de Tkinter y punto de entrada del usuario.
	Incluye buscador, tabla, alta, edicion, login y borrado multiple desde las
	filas seleccionadas, con confirmacion previa.

## Ejecutar

Desde la carpeta raiz del proyecto:

```powershell
python .\ApliTwiRob\main.py
```

La base de datos se crea automaticamente en `ApliTwiRob/data/twitter.db` la
primera vez que se inicia la aplicacion.

## Requisitos

- Python 3.10 o superior.
- Tkinter, incluido normalmente en la instalacion de Python para Windows.

No requiere paquetes externos.