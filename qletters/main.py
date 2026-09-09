def run(letters: str) -> list[str]:
    # 1. Si hay un espacio (policía), nos quedamos solo con lo que hay después del último
    if ' ' in letters:
        letters = letters.split(' ')[-1]
        
    
    mayusculas = [letra for letra in letters if letra.isupper()]
    minusculas = [letra for letra in letters if letra.islower()]


    return mayusculas + minusculas


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)