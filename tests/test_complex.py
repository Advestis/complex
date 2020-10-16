from complex import Complex


def test_init():
    znumber = Complex(3, 4)
    assert znumber.a == 3
    assert znumber.b == 4
    assert int(znumber.r) == 5
