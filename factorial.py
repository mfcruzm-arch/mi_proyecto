LIMIT = 10
factorial = 1

for i in range(1, LIMIT + 1):
    factorial = factorial * i
    print(f"Paso {i}: {factorial}")

print(f"El factorial final de {LIMIT} es: {factorial}")