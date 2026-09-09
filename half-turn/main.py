def run(word1: str, word2: str) -> str:
    # Calculamos el índice medio truncado para cada palabra
    half1 = len(word1) // 2
    half2 = len(word2) // 2

    # Tomamos la primera mitad de word1 y la segunda mitad de word2
    result = word1[:half1] + word2[half2:]

    return result


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)