def run(values: list) -> int:
    min_value = values[0]

    for value in values[1:]:
        if value < min_value:
            min_value = value

    return min_value


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)
