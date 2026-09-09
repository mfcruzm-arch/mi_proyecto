def run(A: list, B: list) -> list:
    return [
        [sum(A[row][index] * B[index][column] for index in range(len(B)))
         for column in range(len(B[0]))]
        for row in range(len(A))
    ]


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import vendor

    vendor.launch(run)
