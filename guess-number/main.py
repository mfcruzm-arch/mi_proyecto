def run(target_number: int) -> None:
    intento = 0
    numero = 0
    while(True):
        intento += 1
        numero = int(input("Introduzca número: "))
        if(numero == target_number):
            print ("Enhorabuena has encontrado el número en", intento, "intentos")
            break
        elif numero > target_number:
            print ("Menor")
        else:
            print ("Mayor")

# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    main()