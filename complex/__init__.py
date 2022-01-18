"""Implementation of the notion of complex number

>>> from complex import Complex, i
>>> print(i)
0.0 + 1.0i
>>> znumber = Complex(3, 4)
>>> znumber_fromstring = Complex(s="3+4i")
>>> znumber_fromstring_cos = Complex(s="3cos(4) + 4isin(1)")
>>> znumber_fromstring_exp = Complex(s="5e^3.1415926i")
>>> znumber + znumber_fromstring
>>> z_conj = znumber.conjugate
"""


from .complex import Complex, i

try:
    from ._version import __version__
except ImportError:
    pass
