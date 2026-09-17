class UsuarioRedSocial:
    def __init__(self, nombre, amigos, publicaciones):
        self.__nombre = nombre
        self.__amigos = amigos
        self.__publicaciones = publicaciones

    def mostrar_info(self):
        print(f"Nombre: {self.__nombre}")
        print(f"Amigos: {', '.join(self.__amigos) if self.__amigos else 'Ninguno'}")
        print(f"Publicaciones: {', '.join(self.__publicaciones) if self.__publicaciones else 'Ninguna'}")


nombre = input("Introduce tu nombre: ").strip()
amigos = []

for i in range(1, 4):
    nombre_amigo = input(f"Introduce el nombre del amigo {i}: ").strip()
    if nombre_amigo:
        amigos.append(nombre_amigo)

publicaciones_texto = input("Introduce tus publicaciones separadas por comas: ").strip()
publicaciones = [publicacion.strip() for publicacion in publicaciones_texto.split(",") if publicacion.strip()]

usuario = UsuarioRedSocial(nombre, amigos, publicaciones)
usuario.mostrar_info()

