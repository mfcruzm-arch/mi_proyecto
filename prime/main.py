def run(n: int) -> bool:
    if n <= 1:
        is_prime = False
    else:
        is_prime = True
        for i in range(2, n):
            if n % i == 0:
                is_prime = False
                break
                
    return is_prime


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    # Tu prueba personalizada aquí:
    print(run(7))  # Imprimirá True

    import vendor
    vendor.launch(run)