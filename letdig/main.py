def run(text: str) -> tuple[int, int]:
    num_letters = 0
    num_digits = 0
    
    for char in text:
        if char.isalpha():
            num_letters += 1
        elif char.isdigit():
            num_digits += 1
            
    return num_letters, num_digits


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)