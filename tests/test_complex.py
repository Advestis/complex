from complex import Complex, i
import math


def test_init():
    print("\n\n\nTesting init...\n")
    znumber = Complex(3, 4)
    assert znumber.a == 3
    assert znumber.b == 4
    assert int(znumber.r) == 5


def test_i():
    print("\n\n\nTesting i...\n")
    z = 3 + 2 * i
    assert z == Complex(3, 2)


def test_expi():
    print("\n\n\nTesting expi...\n")
    z = 3 * math.exp(2 * i)
    assert z == Complex(r=3, theta=2)


def test_logi():
    print("\n\n\nTesting logi...\n")
    z = Complex(r=3, theta=2)
    assert math.log(z) == Complex(a=math.log(3), b=2)
