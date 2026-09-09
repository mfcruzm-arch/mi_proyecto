def run(input_date: str, base_year: int) -> str:
    month, day, year = input_date.split('/')
    full_year = int(year) + base_year
    return f"{day}-{month}-{full_year}"


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)