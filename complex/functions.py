"""Some arithmetic and trigonometric-related functions"""

import math
from typing import Tuple


def compatible_numbers(n_1: float, n_2: float, threshold: float = 1e-8) -> bool:
    """Returns True if both numbers are equal or almost the same"""
    if n_1 == n_2:
        return True

    if abs((n_1 - n_2) / n_1) < threshold:
        return True

    return False


def r_theta_from_ab(real: float, imaginary: float) -> Tuple[float, float]:
    """Returns norm and argument of a complex number from the real and imaginary parts

    Parameters
    ----------
    real: float
    imaginary: float

    Returns
    -------
    Tuple[float, float]
        Norm and argument
    """

    norm = math.sqrt(real ** 2 + imaginary ** 2)
    if imaginary > 0:
        theta = math.acos(real / norm)
    else:
        theta = -math.acos(real / norm)

    if abs(theta) < 1e-15:
        theta = 0.0
    return norm, theta


def ab_from_r_theta(norm: float, theta: float) -> Tuple[float, float]:
    """Returns real and imaginary part of real complex number from its norm and argument

    Parameters
    ----------
    norm: float
    theta: float

    Returns
    -------
    Tuple[float, float]
        real and imaginary parts
    """
    real = norm * math.cos(theta)
    imaginary = norm * math.sin(theta)
    if abs(real) < 1e-15:
        real = 0.0
    if abs(imaginary) < 1e-15:
        imaginary = 0.0
    return real, imaginary
