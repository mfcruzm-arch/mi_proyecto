#pregunta 1: Conversor de Temperatura

def celsius_a_fahrenheit(celsius: float) -> float:
    return (celsius * 9/5) + 32

#pregunta 2: Clasificacion de Edad

def clasificar_edad(edad: int) -> str:
    if edad < 0:
        return "Edad no valida"
    elif 0 <= edad <= 12:
        return "Infantil"
    elif 13 <= edad <= 17:
        return "Adolescente"
    elif 18 <= edad <= 64:
        return "Adulto"
    else:
        return "Adulto Mayor"

#Pregunta 3: Suma de Números Pares

def sumar_pares(lista_numero: list[int]) -> int:
    return sum(x for x in lista_numero if x % 2 == 0)


#Pregunta 4: Clase Jugador

class Jugador:
    def __init__(self, nombre: str, dorsal: int | None = None):
        self.nombre = nombre
        self.dorsal = dorsal
        self.convocado = False
        self.faltas = 0

    def convocar(self) -> None:
        self.convocado = True

    def desconvocar(self) -> None:
        self.convocado = False

    def asignar_dorsal(self, nuevo_dorsal: int) -> None:
        self.dorsal = nuevo_dorsal

    def registrar_falta(self) -> None:
        self.faltas += 1

    def reiniciar_faltas(self) -> None:
        self.faltas = 0


#Pregunta 5: Clase EquipoFutbol

class EquipoFutbol:
    def __init__(self, nombre_equipo: str):
        self.nombre = nombre_equipo
        self.jugadores: list[Jugador] = []

    def fichar_jugador(self, jugador: Jugador) -> None:
        self.jugadores.append(jugador)

    def convocar_todos(self) -> None:
        for j in self.jugadores:
            j.convocar()

    def obtener_sancionados(self, limite_faltas: int = 3) -> list[str]:
        sancionados = []
        for j in self.jugadores:
            if j.faltas >= limite_faltas:
                sancionados.append(j.nombre)
        return sancionados


# ==========================================================
# VERIFICACIÓN Y SALIDA EXACTA
# ==========================================================

equipo = EquipoFutbol("Real Madrid")

j1 = Jugador("Luka Modric", 10)
j2 = Jugador("Jude Bellingham", 5)

equipo.fichar_jugador(j1)
equipo.fichar_jugador(j2)

print(f"Equipo: {equipo.nombre}")
print(f"Numeros de Jugadores: {len(equipo.jugadores)}")
for j in equipo.jugadores:
    print(f"-{j.nombre} (Dorsal: {j.dorsal})")