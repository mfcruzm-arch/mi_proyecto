class Fabrica:
    def __init__(self, llantas: int, puertas: int, color:str, precio: float):
        self.llantas = llantas
        self.puertas = puertas
        self.color = color
        self.precio = precio

    def mostrar_caracteristicas(self):
        print(f"Llantas: {self.llantas}")
        print(f"Color: {self.color}")
        print(f"Precio: ${self.precio:.2f} Є")

class Moto(Fabrica):
    def __init__(self, color: str, precio: float, llantas: int = 2):
        super().__init__(llantas, 0, color, precio)

    def mostrar_datos(self):
        print("== DATOS DE LA MOTO ==")
        self.mostrar_caracteristicas()

class Carro(Fabrica):
    def __init__(self, color:str, precio: float, llantas: int = 4, puertas: int = 4):
        super().__init__(llantas, puertas, color, precio)

    def mostrar_datos(self):
        print("== DATOS DEL CARRO ==")
        self.mostrar_caracteristicas()

if __name__ == "__main__":
    # Crear un objeto Moto
    moto1 = Moto(color="Rojo", precio=1500.00)
    moto1.mostrar_datos()

    print()  # Línea en blanco para separar la salida

    # Crear un objeto Carro
    carro1 = Carro(color="Azul", precio=20000.00)
    carro1.mostrar_datos()
         