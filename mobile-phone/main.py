# TODO
class MobilePhone:
    # Datos básicos que describen el teléfono.
    manufacturer: str = ''
    screen_size: float = 0.0
    num_cores: int = 0
    # Lista de aplicaciones instaladas y estado de encendido.
    apps: list[str] = []
    status: bool = False

    # Crea un teléfono con sus características iniciales.
    def __init__(self, manufacturer: str, screen_size: float, num_cores: int):
        self.manufacturer = manufacturer
        self.screen_size = screen_size
        self.num_cores = num_cores
        # Cada teléfono debe tener su propia lista de aplicaciones.
        self.apps = []
        self.status = False

    # Enciende el teléfono.
    def power_on(self):
        self.status = True

    # Apaga el teléfono.
    def power_off(self):
        self.status = False

    # Instala una o varias aplicaciones, evitando duplicados.
    def install_app(self, *apps: str):
        for app in apps:
            if app not in self.apps:
                self.apps.append(app)

    # Desinstala una o varias aplicaciones si están instaladas.
    def uninstall_app(self, *apps: str):
        for app in apps:
            if app in self.apps:
                self.apps.remove(app)
                