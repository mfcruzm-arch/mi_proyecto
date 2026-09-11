class Laboratorio:
    def __init__(self, nombre, puertas):
        self.__nombre = nombre
        self.__puertas = list(puertas)

    def get_nombre(self):
        return self.__nombre

    def get_puertas(self):
        return list(self.__puertas)

    def encender_luces(self):
        resultado = list(self.__puertas)
        i = 0

        while i < len(self.__puertas):
            if self.__puertas[i] <= 0:
                i += 1
                continue

            frecuencia = self.__puertas[i]
            siguiente = i + 1

            while (siguiente < len(self.__puertas)
                   and self.__puertas[siguiente] == 0):
                siguiente += 1

            if (siguiente < len(self.__puertas)
                    and self.__puertas[siguiente] == frecuencia):
                for posicion in range(i + 1, siguiente):
                    resultado[posicion] = frecuencia

            i = siguiente

        return resultado
