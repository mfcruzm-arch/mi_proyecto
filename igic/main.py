def run(price_with_igic: float, igic: float) -> float:
    clean_price = price_with_igic / (1 + igic / 100)
    clean_price = round(clean_price, 2)
    print(clean_price)
    return clean_price


# Prueba interactiva desde consola
if __name__ == '__main__':
    precio = float(input("Introduce el precio con IGIC: "))
    porcentaje = float(input("Introduce el porcentaje de IGIC: "))
    run(precio, porcentaje)