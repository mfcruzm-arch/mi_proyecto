def run(text: str) -> str:
    # Convertir a minúsculas
    text = text.lower()
    
    # Limpiar caracteres alfanuméricos
    limpio = ""
    for char in text:
        if char.isalnum():
            limpio += char
            
    return limpio


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)