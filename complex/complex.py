"""Contains the class Complex, which implements the notion of complex number"""


import math
from typing import Union, Optional
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from complex.functions import compatible_numbers, r_theta_from_ab, ab_from_r_theta


class ForbiddenAssignmentError(Exception):
    """Home-made class used to tell the user that Complex does not allow for new attributes assignment. I.e, one
    can do 'some_complex_number.a = 0', but not 'some_complex_number.foo = 0', for 'foo' is not a known attribute of
    the class."""


PROTECTED_ATTRIBUTES = [
    "_Complex__real",
    "_Complex__imaginary",
    "_Complex__norm",
    "_Complex__theta",
    "_Complex__cartesian",
]
ATTRIBUTES = ["real", "imaginary", "norm", "theta", "cartesian"]


class Complex:
    """Complex Number

    Attributes
    ----------
    real: float
    imaginary: float
    norm: float
    theta: float
    """

    def __init__(
        self,
        real: Optional[Union[float, "Complex"]] = None,
        imaginary: Optional[float] = None,
        norm: Optional[float] = None,
        theta: Optional[float] = None,
        from_string: Optional[str] = None,
        from_complex: Optional["Complex"] = None,
    ):
        """
        You can initialise the Complex class in one of the following ways:\n
          * By giving another complex number as first argument or a *from_complex* argument\n
          * By giving real and imaginary part as first two arguments\n
          * By giving explicitely *norm=* and *theta=*\n
          * By giving a mathematical expression as the *from_string* argument\n
        See example below.
        No matter the method you choose, the real and imaginary parts along with norm and argument are set.
        If you modify any of those, the other 3 will be modified accordingly.

        Parameters
        ----------
        real: Optional[Union[float, "Complex"]]
        imaginary: Optional[float]
        norm: Optional[float]
        theta: Optional[float]
        from_string: Optional[str]
            String representation
        from_complex: Optional[Complex]
            Another complex number to copy

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(znumber.real)
        3.0
        >>> print(znumber.imaginary)
        4.0
        >>> print(znumber.norm)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(3, 4, 5, 0.9)
        Traceback (most recent call last):
          ...
        ValueError: You specified both cartesian and trigo representations but the values are not compatible
        >>> znumber = Complex(3, 4, 5, 0.9272952180016123)

        >>> znumber = Complex(norm=5, theta=0.9272952180016123)
        >>> print(znumber.real)
        3.0
        >>> print(znumber.imaginary)
        4.0
        >>> print(znumber.norm)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(from_string="3+4i")
        >>> print(znumber.real)
        3.0
        >>> print(znumber.imaginary)
        4.0
        >>> print(znumber.norm)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(from_string="3")
        >>> print(znumber.real)
        3.0
        >>> print(znumber.imaginary)
        0.0
        >>> print(znumber.norm)
        3.0
        >>> print(znumber.theta)
        0.0

        >>> znumber = Complex(from_string="4i")
        >>> print(znumber.real)
        0.0
        >>> print(znumber.imaginary)
        4.0
        >>> print(znumber.norm)
        4.0
        >>> print(znumber.theta)
        1.5707963267948966

        >>> znumber = Complex(from_string="3cos(0)")
        >>> print(znumber.real)
        3.0
        >>> print(znumber.imaginary)
        0.0
        >>> print(znumber.norm)
        3.0
        >>> print(znumber.theta)
        0.0

        >>> znumber = Complex(from_string="4isin(1.5707963267948966)")
        >>> print(znumber.real)
        0.0
        >>> print(znumber.imaginary)
        4.0
        >>> print(znumber.norm)
        4.0
        >>> print(znumber.theta)
        1.5707963267948966

        >>> # In case your string can not be a complex (here we would have two different r for instance),
        >>> # it is the part in 'cos' that is used.
        >>> znumber = Complex(from_string="3cos(4) + 4isin(1)")
        >>> print(znumber.real)
        -1.960930862590836
        >>> print(znumber.imaginary)
        -2.2704074859237844
        >>> print(znumber.norm)
        3.0
        >>> print(znumber.theta)
        4.0

        >>> znumber = Complex(from_string="3 + 4 * i")
        >>> print(znumber.real)
        3.0
        >>> print(znumber.imaginary)
        4.0
        >>> print(znumber.norm)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(from_string="5e^0.9272952180016123i")
        >>> print(znumber.real)
        3.0
        >>> print(znumber.imaginary)
        4.0
        >>> print(znumber.norm)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(from_string="5*(cos(0.9272952180016123i) + isin(0.9272952180016123i)")
        >>> print(znumber.real)
        3.0
        >>> print(znumber.imaginary)
        4.0
        >>> print(znumber.norm)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber_2 = Complex(from_complex=znumber)
        >>> print(znumber_2.real)
        3.0
        >>> print(znumber_2.imaginary)
        4.0
        >>> print(znumber_2.norm)
        5.0
        >>> print(znumber_2.theta)
        0.9272952180016123

        >>> znumber_2 = Complex(znumber)
        >>> print(znumber_2.real)
        3.0
        >>> print(znumber_2.imaginary)
        4.0
        >>> print(znumber_2.norm)
        5.0
        >>> print(znumber_2.theta)
        0.9272952180016123
        """

        if isinstance(real, Complex):
            from_complex = real
            real = None
            imaginary = None
            norm = None
            theta = None

        if norm is not None and norm < 0:
            raise ValueError("A complex number's norm cannot be negative!")

        self.__real = float(real) if real is not None else None
        self.__imaginary = float(imaginary) if imaginary is not None else None
        self.__norm = float(norm) if norm is not None else None
        self.__theta = float(theta) if theta is not None else None
        self.__cartesian = False

        self.__init(from_string, from_complex)

    def __init(self, from_string: Union[None, str], from_complex: Union[None, "Complex"]):

        if from_complex:
            self.real = from_complex.real
            self.imaginary = from_complex.imaginary
            self.norm = from_complex.norm
            self.theta = from_complex.theta
            self.__cartesian = from_complex.cartesian
        elif from_string:
            self._guess_repr_from_string(from_string)
        else:
            self._guess_repr()

    @property
    def conjugate(self) -> "Complex":
        """Returns the complex conjugate of this complex number

        Returns
        -------
        Complex
        """
        if self.cartesian is True:
            # pylint: disable=invalid-unary-operand-type
            return Complex(self.real, -self.imaginary)
        # pylint: disable=invalid-unary-operand-type
        return Complex(norm=self.norm, theta=-self.theta)

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_repr()

    def to_string(self, repres: str = "cartesian") -> str:
        """Human-readable str

        Parameters
        ----------
        repres: str
            Can be "cartesion", "exp" or "trigo"

        Returns
        -------
        str

        Examples
        --------
        >>> z = Complex(3, 3)
        >>> print(z)
        3.0 + 3.0i
        >>> print(z.to_string("trigo"))
        4.242640687119285 * (cos(0.7853981633974483) + isin(0.7853981633974483))
        >>> print(z.to_string("exp"))
        4.242640687119285e^0.7853981633974483i

        Raises
        ------
        ValueError
            If given 'repres' argument is not "cartesian", "trigo" nor "exp"
        """
        bsign = "+" if self.imaginary > 0 else "-"
        if repres == "cartesian":
            return f"{self.real} {bsign} {abs(self.imaginary)}i"
        if repres == "trigo":
            return f"{self.norm} * (cos({self.theta}) + isin({self.theta}))"
        if repres == "exp":
            return f"{self.norm}e^{self.theta}i"
        raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def to_repr(self, repres: str = "cartesian") -> str:
        """str readable by exec() or eval()

        Parameters
        ----------
        repres: str
            Can be "cartesion", "exp" or "trigo"

        Returns
        -------
        str

        Examples
        --------
        >>> z = Complex(3, 3)
        >>> print(repr(z))
        3.0 + 3.0 * i
        >>> print(z.to_repr("trigo"))
        4.242640687119285 * (cos(0.7853981633974483) + i * sin(0.7853981633974483))
        >>> print(z.to_repr("exp"))
        4.242640687119285 * e ** (0.7853981633974483 * i)

        Raises
        ------
        ValueError
            If given 'repres' argument is not "cartesian", "trigo" nor "exp"
        """
        bsign = "+" if self.imaginary > 0 else "-"
        if repres == "cartesian":
            return f"{self.real} {bsign} {abs(self.imaginary)} * i"
        if repres == "trigo":
            return f"{self.norm} * (cos({self.theta}) + i * sin({self.theta}))"
        if repres == "exp":
            return f"{self.norm} * e ** ({self.theta} * i)"
        raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def to_latex(self, repres: str = "cartesian") -> str:
        """Formats the complex number into a LaTeX expression

        Parameters
        ----------
        repres: str
            Can be "cartesion", "exp" or "trigo"

        Returns
        -------
        str

        Examples
        --------
        >>> z = Complex(3, 3)
        >>> print(z.to_latex())
        $3.0 + 3.0i$
        >>> print(z.to_latex("trigo"))
        $4.242640687119285 \\times (\\cos(0.7853981633974483) + i \\sin(0.7853981633974483))$
        >>> print(z.to_latex("exp"))
        $4.242640687119285 \\text{e}^{0.7853981633974483 i}$

        Raises
        ------
        ValueError
            If given 'repres' argument is not "cartesian", "trigo" nor "exp"
        """
        if repres == "cartesian":
            return f"${self.real} + {self.imaginary}i$"
        if repres == "trigo":
            return f"${self.norm} \\times (\\cos({self.theta}) + i \\sin({self.theta}))$"
        if repres == "exp":
            return f"${self.norm} \\text{{e}}^{{{self.theta} i}}$"
        raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def round(self, rount_to: int) -> "Complex":
        """Returns another complex number with rounded attributes using builting `round` method.

        Parameters
        ----------
        rount_to: int

        Returns
        -------
        Complex

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.round(rount_to=2))
        3.12 + 4.79i
        >>> print((znumber.round(rount_to=2, repres="exp")).to_string("exp"))
        5.72e^0.99i

        """
        if self.cartesian is True:
            return Complex(round(self.real, rount_to), round(self.imaginary, rount_to))
        return Complex(norm=round(self.norm, rount_to), theta=round(self.theta, rount_to))

    def ceil(self) -> "Complex":
        """Use `math.ceil` method to create a new complex number

        Returns
        -------
        Complex

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.ceil())
        4.0 + 5.0i
        >>> print((znumber.ceil(repres="exp")).to_string("exp"))
        6.0e^1.0i

        """
        if self.cartesian is True:
            return Complex(math.ceil(self.real), math.ceil(self.imaginary))
        return Complex(norm=math.ceil(self.norm), theta=math.ceil(self.theta))

    def floor(self) -> "Complex":
        """Use `math.floor` method to create a new complex number

        Returns
        -------
        Complex

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.floor())
        3.0 + 4.0i
        >>> print((znumber.floor(repres="exp")).to_string("exp"))
        5.0e^0.0i

        """
        if self.cartesian is True:
            return Complex(math.floor(self.real), math.floor(self.imaginary))
        return Complex(norm=math.floor(self.norm), theta=math.floor(self.theta))

    def trunc(self) -> "Complex":
        """Use `math.trunc` method to create a new complex number

        Returns
        -------
        Complex

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.trunc())
        3.0 + 4.0i
        >>> print((znumber.trunc(repres="exp")).to_string("exp"))
        5.0e^0.0i
        """
        if self.cartesian is True:
            return Complex(math.trunc(self.real), math.trunc(self.imaginary))
        return Complex(norm=math.trunc(self.norm), theta=math.trunc(self.theta))

    def plot(self, fig: Optional[Figure] = None, **kwargs) -> Figure:
        """Plots the complex number and returns a `plotly.graph_objs.Figure` object

        Parameters
        ----------
        fig: Optional[Figure]
            Figure to plot in. Will create one if not specified
        kwargs
            Any keyword argument to pass to `plotly.express.scatter` (if *fig* is None) or
            `plotly.graph_objects.Scatter` (if *fig* is not None)

        Returns
        -------
        Figure
        """
        if fig is None:
            fig = px.scatter(
                pd.DataFrame(columns=["$\\mathbb{R}$", "$\\mathbb{C}$"], data=[[self.real, self.imaginary]]),
                x="$\\mathbb{R}$",
                y="$\\mathbb{C}$",
                **kwargs,
            )
        else:
            fig.add_trace(go.Scatter(x=[self.real], y=[self.imaginary], mode="markers", **kwargs))
        return fig

    @property
    def real(self) -> float:
        """Real part.

        If modified, recomputes norm and argument by using `complex.Complex.r_theta_from_ab`
        """
        if str(self.__real) == "-0.0":
            return 0.0
        return self.__real

    @real.setter
    def real(self, value) -> None:
        self.__real = value
        if self.real is None or self.imaginary is None:
            self.__norm = None
            self.__theta = None
        else:
            self.__norm, self.__theta = r_theta_from_ab(self.real, self.imaginary)

    @property
    def imaginary(self) -> float:
        """Imaginary part.

        If modified, recomputes norm and argument by using `complex.Complex.r_theta_from_ab`
        """
        if str(self.__imaginary) == "-0.0":
            return 0.0
        return self.__imaginary

    @imaginary.setter
    def imaginary(self, value) -> None:
        self.__imaginary = value
        if self.real is None or self.imaginary is None:
            self.__norm = None
            self.__theta = None
        else:
            self.__norm, self.__theta = r_theta_from_ab(self.real, self.imaginary)

    @property
    def norm(self) -> float:
        """Norm.

        If modified, recomputes real and imaginary parts by using `complex.Complex.ab_from_r_theta`
        """
        if str(self.__norm) == "-0.0":
            return 0.0
        return self.__norm

    @norm.setter
    def norm(self, value) -> None:
        self.__norm = value
        if self.norm is None or self.theta is None:
            self.__real = None
            self.__imaginary = None
        else:
            self.__real, self.__imaginary = ab_from_r_theta(self.norm, self.theta)

    @property
    def theta(self) -> float:
        """Argument.

        If modified, recomputes real and imaginary parts by using `complex.Complex.ab_from_r_theta`
        """
        if str(self.__theta) == "-0.0":
            return 0.0
        return self.__theta

    @theta.setter
    def theta(self, value) -> None:
        self.__theta = value
        if self.norm is None or self.theta is None:
            self.__real = None
            self.__imaginary = None
        else:
            self.__real, self.__imaginary = ab_from_r_theta(self.norm, self.theta)

    @property
    def cartesian(self):
        """Is true if the complex number was created from real and imaginary parts, and not from norm and thera"""
        return self.__cartesian

    # Comparison

    def __eq__(self, other: Union[int, float, "Complex", str]) -> bool:
        """

        Example
        -------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(norm=5, theta=0.9272952180016123)
        >>> znumber == znumber2
        True

        """
        if isinstance(other, str):
            other = Complex(from_string=other)
        if isinstance(other, Complex):
            if self.real == other.real and self.imaginary == other.imaginary:
                return True
            if self.norm == other.norm and self.theta == other.theta:
                return True
        elif self.real == other:
            return True
        return False

    def __ne__(self, other: Union[int, float, "Complex", str]) -> bool:
        """

        Example
        -------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(norm=5, theta=0.9272952180016123)
        >>> znumber != znumber2
        False

        """
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        raise ArithmeticError("No order relation defined between complex numbers")

    def __gt__(self, other) -> bool:
        raise ArithmeticError("No order relation defined between complex numbers")

    def __le__(self, other) -> bool:
        raise ArithmeticError("No order relation defined between complex numbers")

    def __ge__(self, other) -> bool:
        raise ArithmeticError("No order relation defined between complex numbers")

    # Unary arithmetic operators

    def __pos__(self) -> "Complex":
        return self

    def __neg__(self) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> z2 = -znumber
        >>> print(z2)
        -3.0 - 4.0i

        """
        # pylint: disable=invalid-unary-operand-type
        return Complex(real=-self.real, imaginary=-self.imaginary)

    def __abs__(self) -> float:
        return self.norm

    def __round__(self, round_to: int = 0) -> "Complex":
        return self.round(rount_to=round_to)

    def __floor__(self) -> "Complex":
        return self.floor()

    def __ceil__(self) -> "Complex":
        return self.ceil()

    def __trunc__(self) -> "Complex":
        return self.trunc()

    # Normal arithmetic operators

    def __add__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(5, 6)
        >>> print(znumber + znumber2)
        8.0 + 10.0i
        >>> znumber2 = "5 + 6i"
        >>> print(znumber + znumber2)
        8.0 + 10.0i
        >>> znumber2 = 5
        >>> print(znumber + znumber2)
        8.0 + 4.0i

        """
        new = Complex(self)

        if isinstance(other, str):
            other = Complex(from_string=other)
        if isinstance(other, Complex):
            new.real = new.real + other.real
            new.imaginary = new.imaginary + other.imaginary
        else:
            new.real = new.real + other
        return new

    def __sub__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(5, 6)
        >>> print(znumber - znumber2)
        -2.0 - 2.0i
        >>> znumber2 = "5 + 6i"
        >>> print(znumber - znumber2)
        -2.0 - 2.0i
        >>> znumber2 = 5
        >>> print(znumber - znumber2)
        -2.0 + 4.0i

        """
        new = Complex(self)

        if isinstance(other, str):
            other = Complex(from_string=other)
        if isinstance(other, Complex):
            new.real = new.real - other.real
            new.imaginary = new.imaginary - other.imaginary
        else:
            new.real = new.real - other
        return new

    def __mul__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(norm=3, theta=4)
        >>> znumber2 = Complex(norm=5, theta=6)
        >>> print((znumber * znumber2).to_string("exp"))
        15.0e^10.0i
        >>> znumber2 = "5e^6i"
        >>> print((znumber * znumber2).to_string("exp"))
        15.0e^10.0i
        >>> znumber2 = 5
        >>> print((znumber * znumber2).to_string("exp"))
        15.0e^4.0i

        """
        new = Complex(self)

        if isinstance(other, str):
            other = Complex(from_string=other)
        if isinstance(other, Complex):
            new.norm = new.norm * other.norm
            new.theta = new.theta + other.theta
        else:
            new.norm = new.norm * other
        return new

    def __truediv__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(norm=3, theta=4)
        >>> znumber2 = Complex(norm=5, theta=6)
        >>> print((znumber / znumber2).to_string("exp"))
        0.6e^-2.0i
        >>> znumber2 = "5e^6i"
        >>> print((znumber / znumber2).to_string("exp"))
        0.6e^-2.0i
        >>> znumber2 = 5
        >>> print((znumber / znumber2).to_string("exp"))
        0.6e^4.0i

        """
        new = Complex(self)

        if isinstance(other, str):
            other = Complex(from_string=other)
        if isinstance(other, Complex):
            new.norm = new.norm / other.norm
            new.theta = new.theta - other.theta
        else:
            new.norm = new.norm / other
        return new

    def __pow__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(norm=3, theta=4)
        >>> znumber2 = Complex(norm=5, theta=6)
        >>> print((znumber ** znumber2).to_string("exp"))
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Complex' and 'Complex'
        >>> znumber2 = "5e^6i"
        >>> print((znumber ** znumber2).to_string("exp"))
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Complex' and 'str'
        >>> znumber2 = 5
        >>> print((znumber ** znumber2).to_string("exp"))
        243.0e^20.0i

        """
        new = Complex(self)

        if isinstance(other, (str, Complex)):
            return NotImplemented
        new.norm = new.norm ** other
        new.theta = new.theta * other
        return new

    # Reflected arithmetic operators

    def __radd__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(1 + znumber)
        4.0 + 4.0i

        """
        return self + other

    def __rsub__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(1 - znumber)
        2.0 + 4.0i

        """
        return self - other

    def __rmul__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(2 * znumber)
        6.0 + 8.0i

        """
        return self * other

    def __rtruediv__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(3 / znumber)
        0.36 - 0.48i

        """
        return self.conjugate * other / self.norm ** 2

    def __rpow__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        return NotImplemented

    # Augmented assignment

    def __iadd__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> znumber += Complex(5, 6)
        >>> print(znumber)
        8.0 + 10.0i

        """
        return self + other

    def __isub__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> znumber -= Complex(5, 6)
        >>> print(znumber)
        -2.0 - 2.0i

        """
        return self - other

    def __imul__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(norm=3, theta=4)
        >>> znumber *= Complex(norm=5, theta=6)
        >>> print(znumber.to_string("exp"))
        15.0e^10.0i

        """
        return self * other

    def __idiv__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(norm=3, theta=4)
        >>> znumber /= Complex(norm=5, theta=6)
        >>> print(znumber.to_string("exp"))
        0.6e^-2.0i

        """
        return self / other

    def __ipow__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(norm=3, theta=4)
        >>> znumber **= Complex(norm=5, theta=6)
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Complex' and 'Complex'
        >>> znumber **= "5e^6i"
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Complex' and 'str'
        >>> znumber **= 5
        >>> print(znumber.to_string("exp"))
        243.0e^20.0i

        """
        return self ** other

    def __copy__(self) -> "Complex":
        return Complex(from_complex=self)

    def __setattr__(self, key, value):
        """

        Examples
        --------
        >>> z = Complex(3, 4)
        >>> z.norm
        5.0
        >>> z.q = 2
        Traceback (most recent call last):
        ...
        complex.ForbiddenAssignmentError: The Complex class does not allow for new attributes assignment
        >>> z.real = 4
        >>> z.norm
        5.656854249492381
        >>> z.__norm = 4
        Traceback (most recent call last):
        ...
        complex.ForbiddenAssignmentError: The Complex class does not allow for new attributes assignment
        """
        if key not in ATTRIBUTES and key not in PROTECTED_ATTRIBUTES:
            raise ForbiddenAssignmentError("The Complex class does not allow for new attributes assignment")
        super().__setattr__(key, value)

    __deepcopy__ = __copy__

    # Internal methods

    def _guess_repr(self) -> None:
        """From real part, imaginary part, norm and a argument, identifies which representation was used
        to create this complex number. If real and imaginary parts were specified, will find that it is cartesian
        and compute norm and argument. If norm and argument were given, will do the opposite. If something like
        real part and norm was given, or not enough information to create the number, will raise ValueError"""
        self.__cartesian = False
        trigo = False

        if self.__real is not None and self.__imaginary is not None:
            self.__cartesian = True
        if self.__norm is not None and self.__theta is not None:
            trigo = True
        if not self.cartesian and not trigo:
            raise ValueError("Not enough information provided at Complex number creation.")

        if self.cartesian:
            if self.__real is None or self.__imaginary is None:
                norm = None
                theta = None
            else:
                norm, theta = r_theta_from_ab(self.__real, self.__imaginary)
            if trigo:
                # Do not set self.norm and self.theta if trigo representation was found, since they were already
                # specified by the user. Just check that those values are compatible with the given a and b
                if not compatible_numbers(norm, self.__norm) or not compatible_numbers(theta, self.__theta):
                    raise ValueError(
                        "You specified both cartesian and trigo representations but the values are not compatible"
                    )
            else:
                self.real = self.__real
                self.imaginary = self.__imaginary
        # If trigo, then not cartesian too. Set a and b.
        else:
            self.norm = self.__norm
            self.theta = self.__theta

    def _guess_repr_from_string(self, the_string) -> None:
        """Same as `complex.Complex._guess_repr` but using a string as input"""
        the_string = the_string.replace("(", "")
        the_string = the_string.replace(")", "")
        the_string = the_string.replace("*", "")
        the_string = the_string.replace("x", "")
        the_string = the_string.replace(" ", "")
        # TODO (pcotte) Add possibility to write something like '3 x e^(i x pi / 4)'
        self.__cartesian = False
        if "e^" in the_string or "exp" in the_string:
            the_string = the_string.replace("i", "")
            if "e^" in the_string:
                self.norm = float(the_string.split("e^")[0])
                self.theta = float(the_string.split("e^")[1])
            else:
                self.norm = float(the_string.split("exp")[0])
                self.theta = float(the_string.split("exp")[1])
        elif "cos" in the_string or "sin" in the_string:
            the_string_splitted = the_string.split("+")[0].replace("i", "")
            if "cos" in the_string_splitted:
                self.norm = float(the_string_splitted.split("cos")[0])
                self.theta = float(the_string_splitted.split("cos")[1])
            else:
                self.norm = float(the_string_splitted.split("sn")[0])
                self.theta = float(the_string_splitted.split("sn")[1])
        else:
            self.__cartesian = True
            if "+" not in the_string:
                if "i" in the_string:
                    self.real = 0.0
                    self.imaginary = float(the_string.replace("i", ""))
                else:
                    self.real = float(the_string)
                    self.imaginary = 0.0
            else:
                self.real = float(the_string.split("+")[0].replace(" ", ""))
                self.imaginary = float(the_string.split("+")[1].replace(" ", "").replace("i", ""))
