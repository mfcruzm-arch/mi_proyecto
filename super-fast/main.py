KM_TO_CM = 100_000
HOURS_TO_SECONDS = 3_600


def run(speed_km_h: float) -> int:
    speed_cm_s = int(speed_km_h * KM_TO_CM / HOURS_TO_SECONDS)
    print(speed_cm_s)
    return speed_cm_s


# Prueba interactiva desde la terminal
if __name__ == '__main__':
    velocidad = float(input("Introduce la velocidad en km/h: "))
    run(velocidad)