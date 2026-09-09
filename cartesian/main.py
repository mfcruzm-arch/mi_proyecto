def run(text1: str, text2: str) -> str:
    # TODO
    cartesian = ""
    for c1 in text1:
        for c2 in text2:
            cartesian += c1 + c2
    return cartesian


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)