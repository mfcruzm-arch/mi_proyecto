def run(input_path: str) -> str:
    # 1. Leer todo el contenido del fichero
    with open(input_path, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    # 2. Definir variables iniciales
    simbolos = ",.;:()"
    longest_word = ""

    # 3. Recorrer y procesar palabra por palabra
    for palabra in texto.split():
        palabra_limpia = palabra.strip(simbolos)
        
        # 4. Comparar (>= para quedarse con la última en caso de empate)
        if len(palabra_limpia) >= len(longest_word):
            longest_word = palabra_limpia

    # 5. Devolver el resultado final
    return longest_word


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)
    