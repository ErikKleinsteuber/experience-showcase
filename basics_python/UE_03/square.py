def squareRoot(x, n=10):
    if n == 1:
        return 1
    else:
        z = squareRoot(x, n - 1)
        return 0.5 * (z + x / z)


print(squareRoot(2, 2))
