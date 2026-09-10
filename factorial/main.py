def factorial(n):
    if not isinstance(n, int) or n < 0:
        return None
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)