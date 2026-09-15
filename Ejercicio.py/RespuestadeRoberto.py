import math
from abc import ABC, abstractmethod


class Poligono(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimetro(self) -> float | None:
        pass


class Triangulo(Poligono):
    def __init__(self, base: float, altura: float):
        self.base: float = base
        self.altura: float = altura

    def area(self) -> float:
        return 0.5 * self.base * self.altura

    def perimetro(self) -> None:
        return None


# Mapeo de nombres de clase a (símbolo, nombre legible)
SIMBOLOS: dict[str, tuple[str, str]] = {
    'Triangulo': ('\u25B2', 'triángulo'),
    'Cuadrado': ('\u25A0', 'cuadrado'),
    'Pentagono': ('\u2B1F', 'pentágono'),
    'Circulo': ('\u25EF', 'círculo')
}


class ListaPoligonos:
    def __init__(self, lista: list[Poligono] | None = None):
        self.lista: list[Poligono] = lista if lista is not None else []

    def __getitem__(self, index: int) -> Poligono:
        return self.lista[index]

    def __setitem__(self, index: int, poligono: Poligono) -> None:
        if index >= len(self.lista):
            self.lista.extend([None] * (index - len(self.lista) + 1))
        self.lista[index] = poligono

    def __len__(self) -> int:
        return len(self.lista)

    def anhadir(self, poligono: Poligono) -> None:
        self.lista.append(poligono)

    def mostrar(self) -> None:
        print("Lista de polígonos:")
        for indice, poligono in enumerate(iterable=self.lista):
            if poligono is None:
                print(f"El elemento de la posición {indice + 1:2} está vacío")
                continue

            # Obtiene el nombre de la clase dinámicamente
            nombre_clase: str = type(poligono).__name__
            icono, nombre: str = SIMBOLOS.get(
                nombre_clase, ('', 'desconocido')
            )

            # Invocación correcta del método perimetro()
            perim: float | None = poligono.perimetro()
            perim_str: str = (
                f"{perim:.2f}"
                if isinstance(perim, (int, float))
                else "N/A"
            )

            print(
                f"{indice + 1:2} | {nombre.capitalize():<10} | "
                f"Posición {indice + 1:2} | Área: {poligono.area():6.2f} | "
                f"Perímetro: {perim_str}"
            )


# --- Prueba de ejecución ---
lista1 = ListaPoligonos()
lista1[0] = Triangulo(base=10.0, altura=5.0)
lista1.anhadir(Triangulo(base=5.0, altura=33.30))

lista1.mostrar()
