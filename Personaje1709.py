class Personaje:
    def __init__(self, nombre, nivel, puntos_vida):
        self.__nombre = nombre
        self.__nivel = nivel
        self.__puntos_vida = puntos_vida

    def mostrar_info(self):
        print(f"Nombre: {self.__nombre}")
        print(f"Nivel: {self.__nivel}")
        print(f"Puntos de Vida: {self.__puntos_vida}")


class Guerrero(Personaje):
    def __init__(self, nombre, nivel, puntos_vida, fuerza, armas="Sin armas"):
        super().__init__(nombre, nivel, puntos_vida)
        self.__fuerza = fuerza
        # Si la cadena viene vacía o solo con espacios, asigna 'Sin armas'
        self.__armas = armas.strip() if armas and armas.strip() else "Sin armas"

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Fuerza: {self.__fuerza}")
        print(f"Armas: {self.__armas}")


class Mago(Personaje):
    def __init__(self, nombre, nivel, puntos_vida, mana):
        super().__init__(nombre, nivel, puntos_vida)
        self.__mana = mana

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Maná: {self.__mana}")


class GestorPersonajes:
    def __init__(self):
        self.__personajes = []

    def agregar_personaje(self, personaje):
        if isinstance(personaje, Personaje):
            self.__personajes.append(personaje)
            print("¡Personaje añadido con éxito!")
        else:
            print("Error: Solo se pueden añadir objetos de tipo Personaje.")

    def mostrar_todos(self):
        if not self.__personajes:
            print("\nNo hay personajes registrados en el gestor.")
            return

        print("\n=== LISTA DE PERSONAJES ===")
        for i, personaje in enumerate(self.__personajes, start=1):
            print(f"\n--- Personaje {i} ---")
            personaje.mostrar_info()


# Programa Principal
gestor = GestorPersonajes()

while True:
    print("\n--- MENÚ DE GESTIÓN ---")
    print("1. Crear Guerrero")
    print("2. Crear Mago")
    print("3. Mostrar todos los personajes")
    print("4. Salir")

    opcion = input("Selecciona una opción (1-4): ")

    if opcion == "1":
        nombre = input("Nombre del guerrero: ")
        nivel = int(input("Nivel: "))
        vida = int(input("Puntos de vida: "))
        fuerza = int(input("Fuerza: "))
        armas = input("Introduce las armas (presiona ENTER si no tiene): ")
        
        guerrero = Guerrero(nombre, nivel, vida, fuerza, armas)
        gestor.agregar_personaje(guerrero)

    elif opcion == "2":
        nombre = input("Nombre del mago: ")
        nivel = int(input("Nivel: "))
        vida = int(input("Puntos de vida: "))
        mana = int(input("Maná: "))
        mago = Mago(nombre, nivel, vida, mana)
        gestor.agregar_personaje(mago)

    elif opcion == "3":
        gestor.mostrar_todos()

    elif opcion == "4":
        print("Saliendo del programa...")
        break

    else:
        print("Opción no válida. Inténtalo de nuevo.")