def sumar(a: float, b: float) -> float:
    """Suma dos números y devuelve el resultado."""
    return a + b


def restar(a: float, b: float) -> float:
    """Resta b de a y devuelve el resultado."""
    return a - b


if __name__ == "__main__":
    print("5 + 3 =", sumar(5, 3))
    print("5 - 3 =", restar(5, 3))
