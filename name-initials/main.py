def run(fullname: str) -> str:
    surnames, names = fullname.split(',', 1)
    words = [names.strip().split()[0]] + surnames.split()
    return ''.join(f'{word[0].upper()}.' for word in words)


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)
