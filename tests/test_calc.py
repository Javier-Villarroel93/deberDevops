from calc.main import sumar, restar


def test_sumar_numeros_positivos():
    assert sumar(2, 3) == 5


def test_sumar_con_negativos():
    assert sumar(-1, 1) == 0


def test_restar_numeros():
    assert restar(5, 3) == 2


def test_restar_resultado_negativo():
    assert restar(3, 5) == -2
