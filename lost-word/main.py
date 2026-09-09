def run(text: str, target_word: str, replace_word: str) -> str:
    # 1. Buscamos el índice donde empieza la palabra objetivo
    idx = text.find(target_word)

    # 2. Reconstruimos el texto troceándolo
    mtext = text[:idx] + replace_word + text[idx + len(target_word):]

    # 3. Devolvemos el texto modificado
    return mtext


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)