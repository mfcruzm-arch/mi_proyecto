from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

# 1. Localizar el CSV en la misma carpeta que este script (Graficos)
ruta_csv = Path(__file__).parent / "Telecomunicaciones.csv"

# Cargar el archivo usando la ruta relativa del script
df = pd.read_csv(ruta_csv, sep=";", encoding="latin-1")

# Limpiar nombres de columnas
df.columns = [col.replace(".", "_") for col in df.columns]

print("¡CSV cargado correctamente!")

# 2. Crear BBDD en memoria
conexion = sqlite3.connect(":memory:")
df.to_sql("telecomunicaciones", conexion, index=False, if_exists="replace")

# 3. Consulta SQL
consulta_sql = """
    SELECT 
        Edad,
        ROUND(AVG(Tiempo_enero + Tiempo_febrero), 2) AS tiempo_medio
    FROM telecomunicaciones
    GROUP BY Edad
    ORDER BY Edad ASC;
"""

resultado = pd.read_sql_query(consulta_sql, conexion)
conexion.close()

# 4. Gráfico
plt.figure(figsize=(10, 5))
plt.plot(
    resultado["Edad"],
    resultado["tiempo_medio"],
    marker="o",
    color="#1f77b4",
    linewidth=2,
)

plt.title("Duración Media de Llamadas por Edad")
plt.xlabel("Edad del Cliente")
plt.ylabel("Tiempo Medio (minutos)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

plt.show()