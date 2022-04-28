

def A(x, y):
    return 4 * x ** 2 - 3 * x * y + 2 * y ** 2 + 24 * x - 20 * y

def dAdx(x, y):
    return 8 * x - 3 * y + 2

def dAdy(x, y):
    return 4(y - 5) - 3 * x

def B(x, y):
    return (1 - y) ** 2 + (x - y ** 2) ** 2

def dBdx(x, y):
    return 2 * (x - y ** 2)

def dBdy(x, y):
    return 2 (-2 * x * y + 2 * y ** 3 + y - 1)

if __name__ == '__main__':
    pass
