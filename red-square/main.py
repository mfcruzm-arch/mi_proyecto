def run(arc_A: float) -> float:
    PI = 3.14
    side = (2 * arc_A) / PI
    area = round(side**2, 10)
    print(area)
    return area


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(func=run)