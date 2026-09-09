import math

PI = 3.14 
def run(radius: float) -> float:
    area: float = PI * (radius**2)
    return area


# DO NOT TOUCH THE CODE BELOW
if __name__ == "__main__":
    import vendor

    vendor.launch(func=run)