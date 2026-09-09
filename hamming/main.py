def run(text1: str, text2: str) -> int:
    # TODO
    if len(text1) != len(text2):
        return -1
    distancia = 0
    for c1, c2 in zip(text1, text2):
        if c1 != c2:
            distancia += 1
    return distancia    
   

# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)
