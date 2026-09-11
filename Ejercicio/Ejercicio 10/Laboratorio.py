class Laboratorio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puertas = list(puertas)

    def encender_luces(self):
        resultado = list(self.puertas)
        n = len(self.puertas)

        for i in range(n):
            if self.puertas[i]> 0:
                