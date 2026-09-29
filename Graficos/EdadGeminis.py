"""Analisis de telecomunicaciones agrupado por edad.

Flujo del programa:
1. Carga el CSV local o lo descarga si no existe junto a este archivo.
2. Normaliza los nombres de columnas para utilizarlos en SQLite.
3. Inserta los datos en una base SQLite temporal en memoria.
4. Ejecuta una consulta SQL agrupada por edad.
5. Muestra los resultados y genera un grafico de lineas.

Este archivo no contiene clases. Utiliza funciones, que son bloques de codigo
con un nombre y una tarea concreta. Separar las tareas en funciones facilita
leer, probar y explicar el programa.
"""

# Path permite trabajar con rutas de archivos de forma segura en Windows,
# Linux y macOS. Se usa para localizar el CSV junto a este archivo.
from pathlib import Path

# sqlite3 permite crear y consultar bases de datos SQLite desde Python.
import sqlite3

# pyplot es el modulo de Matplotlib que permite crear graficos.
import matplotlib.pyplot as plt

# pandas permite leer el CSV y trabajar con los datos en forma de tabla.
import pandas as pd


# Ruta de una posible copia local del CSV. __file__ representa este archivo;
# with_name cambia su nombre por Telecomunicaciones.csv.
CSV_LOCAL = Path(__file__).with_name("Telecomunicaciones.csv")

# Si no existe el CSV local, el programa utilizara esta direccion de Internet.
CSV_URL = (
    "https://raw.githubusercontent.com/VictorGuevaraP/"
    "Mineria-de-datos/master/Telecomunicaciones.csv"
)


def cargar_datos() -> pd.DataFrame:
    """Lee el CSV y devuelve sus datos en una tabla de pandas.

    Una tabla de pandas se llama DataFrame. Se parece a una hoja de calculo:
    tiene filas, columnas y nombres para cada columna.
    """
    # Si existe una copia local, se usa esa copia. Si no, se descarga el CSV
    # desde GitHub. Asi el programa puede funcionar en ambos escenarios.
    origen = CSV_LOCAL if CSV_LOCAL.exists() else CSV_URL

    # sep=';' indica que cada columna esta separada por punto y coma.
    # latin-1 permite leer correctamente las letras acentuadas del archivo.
    return pd.read_csv(origen, sep=";", encoding="latin-1")


def preparar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara los nombres de columnas y comprueba que falten datos clave.

    Recibe el DataFrame leido por ``cargar_datos`` y devuelve una copia lista
    para guardarse en SQLite.
    """
    # copy crea otra tabla para no modificar accidentalmente la tabla original.
    df = df.copy()

    # Los puntos de nombres como Tiempo.enero se cambian por guiones bajos:
    # Tiempo.enero se convierte en Tiempo_enero.
    df.columns = [str(column).strip().replace(".", "_") for column in df.columns]

    # Estas son las columnas que necesita la consulta SQL para funcionar.
    required_columns = {"Edad", "Tiempo_enero", "Tiempo_febrero", "Llamadas"}

    # difference descubre que columnas obligatorias no estan en el CSV.
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        # Se lanza un error explicado en vez de dejar que falle mas adelante.
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Faltan columnas requeridas en el CSV: {missing}")

    # return entrega la tabla preparada a la siguiente funcion.
    return df


def consultar_por_edad(df: pd.DataFrame) -> pd.DataFrame:
    """Guarda los datos en SQLite, ejecuta SQL y devuelve los resultados.

    La funcion recibe una tabla de pandas y devuelve otra tabla de pandas,
    esta vez con una fila por cada edad.
    """
    # ``:memory:`` crea una base de datos temporal que solo vive durante esta
    # ejecucion. No se crea ningun archivo .db en la carpeta del proyecto.
    connection = sqlite3.connect(":memory:")
    try:
        # to_sql copia el DataFrame a una tabla SQL llamada telecomunicaciones.
        # index=False evita guardar el indice de pandas como una columna extra.
        # if_exists='replace' permite repetir el programa sin duplicar datos.
        df.to_sql("telecomunicaciones", connection, index=False, if_exists="replace")

        # Esta es la consulta SQL que resume la informacion:
        # - SELECT elige las columnas que queremos obtener.
        # - AVG calcula un promedio.
        # - ROUND redondea a dos decimales.
        # - Tiempo_enero + Tiempo_febrero suma los dos meses.
        # - COUNT cuenta cuantos clientes hay en cada edad.
        # - GROUP BY crea un grupo separado para cada edad.
        # - ORDER BY ordena las edades de menor a mayor.
        query = """
            SELECT
                Edad,
                ROUND(AVG(Tiempo_enero + Tiempo_febrero), 2)
                    AS tiempo_medio_total,
                ROUND(AVG(Llamadas), 2) AS media_llamadas,
                COUNT(*) AS total_clientes
            FROM telecomunicaciones
            GROUP BY Edad
            ORDER BY Edad ASC;
        """
        # pandas ejecuta la consulta y transforma el resultado en un DataFrame.
        return pd.read_sql_query(query, connection)
    finally:
        # finally garantiza que la conexion se cierre incluso si SQL produce
        # un error. Asi no quedan recursos abiertos.
        connection.close()


def mostrar_grafico(resultados: pd.DataFrame) -> None:
    """Dibuja y muestra una linea con el promedio calculado por SQL.

    ``resultados`` debe contener las columnas Edad y tiempo_medio_total,
    creadas por la consulta de ``consultar_por_edad``.
    """
    # figsize define el ancho y alto del grafico en pulgadas.
    plt.figure(figsize=(10, 5))

    # plot dibuja la linea. El eje X contiene edades y el eje Y los promedios.
    # marker='o' muestra un punto en cada edad calculada.
    plt.plot(
        resultados["Edad"],
        resultados["tiempo_medio_total"],
        marker="o",
        color="#1f77b4",
        linewidth=2,
        label="Tiempo medio total (enero + febrero)",
    )

    # Los siguientes comandos hacen el grafico mas facil de interpretar.
    plt.title("Duracion Media de Llamadas por Edad (Resultado SQL)")
    plt.xlabel("Edad")
    plt.ylabel("Tiempo medio (minutos)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # show abre la ventana grafica. El programa se detiene aqui hasta cerrar
    # la ventana cuando se ejecuta normalmente.
    plt.show()


def main() -> None:
    """Coordina todos los pasos del programa en el orden correcto."""
    # Paso 1: cargar el fichero y convertirlo en un DataFrame.
    datos = cargar_datos()

    # Paso 2: preparar los nombres y comprobar las columnas necesarias.
    datos = preparar_columnas(datos)

    # Pasos 3 y 4: insertar en SQLite y ejecutar la consulta SQL.
    resultados = consultar_por_edad(datos)

    # Paso 5a: mostrar en la terminal la tabla calculada por SQL.
    print(resultados.to_string(index=False))

    # Paso 5b: enviar esos mismos resultados a la funcion del grafico.
    mostrar_grafico(resultados)


# Esta condicion evita que main() se ejecute si otro archivo importa alguna
# funcion de este modulo. Solo se ejecuta automaticamente al lanzar este
# archivo directamente con Python.
if __name__ == "__main__":
    main()