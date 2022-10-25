"""Implementation of the notion of complex number

>>> from complex import Complex, i
>>> print(i)
0.0 + 1.0i
>>> znumber = Complex(3, 4)
>>> znumber_fromstring = Complex(from_string="3+4i")
>>> znumber_fromstring_cos = Complex(from_string="3cos(4) + 4isin(1)")
>>> znumber_fromstring_exp = Complex(from_string="5e^3.1415926i")
>>> znumber + znumber_fromstring
>>> z_conj = znumber.conjugate
"""

import math
from typing import Union, SupportsFloat
from .complex import Complex

from . import _version
__version__ = _version.get_versions()['version']
i = Complex(0, 1)
"""The pure imaginary number"""

mathexp = math.exp


def myexp(number) -> Union[float, Complex]:
    """Overloads `math.exp` to accept complex numbers"""
    if isinstance(number, Complex):
        return mathexp(number.real) * Complex(norm=1, theta=number.imaginary)
    return mathexp(number)


math.exp = myexp

mathlog = math.log


def mylog(number: Union[SupportsFloat, Complex], base=None) -> Union[float, Complex]:
    """Overloads `math.log` to accept complex numbers"""
    if isinstance(number, Complex):
        if base is None:
            return mathlog(number.norm) + i * number.theta
        return mathlog(number.norm, base) + i * number.theta / mathlog(base)
    print(number)
    if base is None:
        return mathlog(number)
    return mathlog(number, base)


math.log = mylog
