# pylint: disable=missing-docstring
import math
import pytest
from complex import Complex, i


# noinspection PyUnusedLocal
@pytest.mark.parametrize(
    "real, imaginary, expected_r, expected_theta",
    [
        (3, 4, 5.0, 0.927295),
        (4, 5, 6.403124, 0.896055)
    ]
)
def test_init(fix1, real, imaginary, expected_r, expected_theta):
    print("\n\n\nTesting init...\n")
    _ = fix1
    znumber = Complex(real, imaginary)
    assert znumber.real == real
    assert znumber.imaginary == imaginary
    assert round(znumber.norm, 6) == expected_r
    assert round(znumber.theta, 6) == expected_theta


# noinspection PyUnusedLocal
@pytest.mark.parametrize(
    "norm, theta, expected_a, expected_b",
    [
        (5, 0.927295218, 3.0, 4.0),
        (-1, -1, None, None)
    ]
)
def test_init_r(fix1, norm, theta, expected_a, expected_b):
    print("\n\n\nTesting init...\n")
    _ = fix1
    if norm < 0:
        with pytest.raises(ValueError):
            Complex(norm=norm, theta=theta)
    else:
        znumber = Complex(norm=norm, theta=theta)
        assert round(znumber.real, 6) == expected_a
        assert round(znumber.imaginary, 6) == expected_b


# noinspection PyUnusedLocal
def test_i(fix1):
    print("\n\n\nTesting i...\n")
    _ = fix1
    number = 3 + 2 * i
    assert number == Complex(3, 2)


# noinspection PyUnusedLocal
def test_expi(fix1):
    print("\n\n\nTesting expi...\n")
    _ = fix1
    number = 3 * math.exp(2 * i)
    assert number == Complex(norm=3, theta=2)


# noinspection PyUnusedLocal
def test_logi(fix1):
    print("\n\n\nTesting logi...\n")
    _ = fix1
    number = Complex(norm=3, theta=2)
    # noinspection PyTypeChecker
    assert math.log(number) == Complex(real=math.log(3), imaginary=2)
