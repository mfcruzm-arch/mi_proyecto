def run(strings: list[str]) -> list[str]:
    # Solución obligatoria utilizando bucles anidados
    result: list[str] = []
    for word in strings:
        for char in word:
            result.append(char)
    return result


# Alternativa sin bucles tradicionales (mediante listas por comprensión anidadas):
# return [char for word in strings for char in word]


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)
    