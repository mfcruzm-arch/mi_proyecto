num_letters = 0
num_digits = 0
text = "JuanGilipollas3000"    
for char in text:
        if char.isalpha():
            num_letters += 1
        elif char.isdigit():
            num_digits += 1
print(num_letters, num_digits)  # Imprimirá (5, 3)
