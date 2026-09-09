def run(current_pos: int, dice: int) -> int:
    new_pos = current_pos + (dice * 2)
    print(new_pos)
    return new_pos


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    posicion = int(input("Introduce la posición actual: "))
    dado = int(input("Introduce el resultado del dado (1-6): "))
    run(posicion, dado)