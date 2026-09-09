def run(text):
    vocales = "aeiouáéíóúAEIOUÁÉÍÓÚ"
    num_vowels = 0
    
    for caracter in text:
        if caracter in vocales:
            num_vowels += 1

    return num_vowels


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)