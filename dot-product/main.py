def run(u: list, v: list) -> float | None:
    if len(u) != len(v):
        return None

    return sum(x * y for x, y in zip(u, v))


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)
