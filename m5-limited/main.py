def run(limit: int) -> None:
    for numero in range(5, limit, 5):
        print(numero)


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)