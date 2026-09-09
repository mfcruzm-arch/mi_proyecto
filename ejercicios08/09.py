import unicodedata

frase = input("Ingresa una frase: ")

# Normalizamos el texto para separar las tildes de las letras
frase_normalizada = unicodedata.normalize('NFD', frase)

# Filtramos eliminando los caracteres de tilde (categoría 'Mn' de Unicode)
sin_tildes = "".join(c for c in frase_normalizada if unicodedata.category(c) != 'Mn')

# Ahora solo pasamos todo a minúsculas y contamos las vocales base
total = sum(1 for letra in sin_tildes.lower() if letra in 'aeiou')

print(f"Cantidad total de vocales: {total}")