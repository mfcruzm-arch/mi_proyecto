class FiguraGeometrica:
    def __init__(self, numerolados, radio, nombre):
        self.numerolados = numerolados
        self.radio = radio
        self.nombre = nombre

    def calculaer_area(self):
        pass


class Cuadrado(FiguraGeometrica):
    def __init__(self, lado):
        super().__init__(numerolados=4, radio=0, nombre="Cuadrado")
        self.lado = lado

    def calcular_area(self):
        return self.lado ** 2

    def calcular_perimetro(self):
        return self.lado * 4


class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        super().__init__(numerolados=0, radio=radio, nombre="Círculo")
        self.radio = radio

    def calcular_area(self):
        import math
        return math.pi * (self.radio ** 2)

    def calcular_perimetro(self):
        import math
        return 2 * math.pi * self.radio


class Triangulo(FiguraGeometrica):
    def __init__(self, base, altura):
        super().__init__(numerolados=3, radio=0, nombre="Triángulo")
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return (self.base * self.altura) / 2

    def calcular_perimetro(self):
        return self.base * 3


class Pentagono(FiguraGeometrica):
    def __init__(self, lado):
        super().__init__(numerolados=5, radio=0, nombre="Pentágono")
        self.lado = lado

    def calcular_area(self):
        import math
        return (5 * self.lado ** 2) / (4 * math.tan(math.pi / 5))

    def calcular_perimetro(self):
        return self.lado * 5


class Rectangulo(FiguraGeometrica):
    def __init__(self, base, altura):
        super().__init__(numerolados=4, radio=0, nombre="Rectángulo")
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura

    def calcular_perimetro(self):
        return 2 * (self.base + self.altura)


class AgregadoPoligonos:
    def __init__(self):
        self.poligonos = []

    def agregar_poligono(self, poligono):
        self.poligonos.append(poligono)

    def calcular_area_total(self):
        return sum(poligono.calcular_area() for poligono in self.poligonos)

    def calcular_perimetro_total(self):
        return sum(poligono.calcular_perimetro() for poligono in self.poligonos)


agregado1 = AgregadoPoligonos() 
agregado1.agregar_poligono(Circulo (3))
agregado1.agregar_poligono(Cuadrado(5))
agregado1.agregar_poligono(Triangulo(4, 6))

agregado2 = AgregadoPoligonos()
agregado2.agregar_poligono(Circulo(3))
agregado2.agregar_poligono(Cuadrado(5))
agregado2.agregar_poligono(Triangulo(4, 6))

agregado3 = AgregadoPoligonos()
agregado3.agregar_poligono(Triangulo(4, 6))
agregado3.agregar_poligono(Pentagono(5))
agregado3.agregar_poligono(Rectangulo(4, 6))

print ("=== Agregado 1 ===")
for poligono in agregado1.poligonos:
    print(f"Polígono: {poligono.nombre}, Área: {poligono.calcular_area()}, Perímetro: {poligono.calcular_perimetro()}")

print("\n=== Agregado 2 ===")
for poligono in agregado2.poligonos:
    print(f"Polígono: {poligono.nombre}, Área: {poligono.calcular_area()}, Perímetro: {poligono.calcular_perimetro()}")

print("\n=== Agregado 3 ===")
for poligono in agregado3.poligonos:
    print(f"Polígono: {poligono.nombre}, Área: {poligono.calcular_area()}, Perímetro: {poligono.calcular_perimetro()}")

            