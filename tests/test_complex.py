from complex import Complex, i
import math
import pytest


@pytest.mark.parametrize(
    "a, b, expected_r",
    [
        (3, 4, 5),
        (4, 5, 6)
    ]
)
def test_init(a, b, expected_r):
    print("\n\n\nTesting init...\n")
    znumber = Complex(a, b)
    assert znumber.a == a
    assert znumber.b == b
    assert int(znumber.r) == expected_r


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
