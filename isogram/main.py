def run(text: str) -> bool:
    vistos = set()
    for char in text.lower():
        if char != '-':
            if char in vistos:
                return False
            vistos.add(char)
    return True


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)