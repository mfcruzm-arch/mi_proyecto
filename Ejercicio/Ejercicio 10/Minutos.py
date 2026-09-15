class GeneradorCommit:
    def __init__(self, minutos: int):
        self.__minutos = minutos

    def obtener_mensaje(self) -> str:
        if self.__minutos == 1:
            return f"Last commit: {self.__minutos} minute ago"
        else:
            return f"Last commit: {self.__minutos} minutes ago"


while True:
    try:
        numero = int(input("Escribe un numero entero entre 0 y 99: "))
        if 0 <= numero <= 99:
            break
        else:
            print("El número debe estar entre 0 y 99.")
    except ValueError:
        print("Error: Debes ingresar obligatoriamente un número entero.")

commit = GeneradorCommit(numero)
print(commit.obtener_mensaje())