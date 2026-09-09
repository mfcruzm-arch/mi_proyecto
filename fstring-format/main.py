def run(value: float) -> str:
    res = f"""{value:.3f}
{value:.6f}
{value:>8.2f}
{value:.6e}
{value:010.4f}
{value:>19.5f}"""

    return res


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)