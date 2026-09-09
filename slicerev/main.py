def run(items: list[int]) -> list[int]:
    # Si la lista está vacía, devolvemos una lista vacía directamente
    if not items:
        return []
    
    # Obtenemos el paso asegurándonos de que no sea 0 y manejando valores negativos si es necesario
    paso = items[len(items) // 2]
    
    if paso == 0:
        paso = 1  # Evita el error de paso cero en el slice
        
    # Troceamos usando valor absoluto para asegurar que avanza desde el principio al final
    result = items[::abs(paso)][::-1]
    
    return result


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)