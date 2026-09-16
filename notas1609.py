class Estudiante:
    def __init__(self, nombre: str, nota: float):
        self.nombre = nombre
        self.nota = nota

    def imprimir_datos(self):
        print(f"Estudiante: {self.nombre}")
        print(f"Nota: {self.nota}")

    def evaluar(self):
        if self.nota >= 5.0:
            print(f"El alumno/a {self.nombre} ha APROBADO.")
        else:
            print(f"El alumno/a {self.nombre} ha REPROBADO.")



if __name__ == "__main__":
    # Crear un objeto Estudiante
    estudiante1 = Estudiante("Juan Pérez", 7.5)
    estudiante2 = Estudiante("María López", 4.8)

    # Imprimir datos y evaluar
    estudiante1.imprimir_datos()
    estudiante1.evaluar()

    print()  # Línea en blanco para separar la salida

    estudiante2.imprimir_datos()
    estudiante2.evaluar()

    