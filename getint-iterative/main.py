def getint():
    valor = None
    while True:
        try:
            return int(input("Give me an integer number:"))
        except ValueError:
            print("Not a valid integer. Try it again!")
        else:
            break

# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(getint)
