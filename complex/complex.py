import math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.graph_objs import Figure
from typing import Union, Tuple, SupportsFloat, Optional


class ForbiddenAssignmentError(Exception):
    pass


PROTECTED_ATTRIBUTES = ["_Complex__a", "_Complex__b", "_Complex__r", "_Complex__theta"]
ATTRIBUTES = ["a", "b", "r", "theta"]
CARTESIAN_ATTRIBUTES = ["a", "b"]


def compatible_numbers(n1: float, n2: float, threshold: float = 1e-8) -> bool:
    """Returns True if both numbers are equal or almost the same"""
    if n1 == n2:
        return True

    if abs((n1 - n2) / n1) < threshold:
        return True

    return False


def r_theta_from_ab(a: float, b: float) -> Tuple[float, float]:
    """Returns norm and argument of a complex number from the real and imaginary parts

    Parameters
    ----------
    a: float
        Real part
    b: float
        Imaginary part

    Returns
    -------
    Tuple[float, float]
        Norm and argument
    """

    r = math.sqrt(a ** 2 + b ** 2)
    if b > 0:
        theta = math.acos(a / r)
    else:
        theta = -math.acos(a / r)

    if abs(theta) < 1e-15:
        theta = 0.0
    return r, theta


def ab_from_r_theta(r: float, theta: float) -> Tuple[float, float]:
    """Returns real and imaginary part of a complex number from its norm and argument

    Parameters
    ----------
    r: float
        Real part
    theta: float
        Imaginary part

    Returns
    -------
    Tuple[float, float]
        real and imaginary parts
    """
    a = r * math.cos(theta)
    b = r * math.sin(theta)
    if abs(a) < 1e-15:
        a = 0.0
    if abs(b) < 1e-15:
        b = 0.0
    return a, b


class Complex:
    """Complex Number

    Attributes
    ----------
    a: float
        Real part
    b: float
        Imaginary part
    r: float
        Norm
    theta: float
        Argument
    """
    def __init__(
        self,
        a: Optional[Union[float, "Complex"]] = None,
        b: Optional[float] = None,
        r: Optional[float] = None,
        theta: Optional[float] = None,
        s: Optional[str] = None,
        z: Optional["Complex"] = None,
    ):
        """
        You can initialise the Complex class in one of the following ways:\n
          * By giving another complex number as first argument or a *z* argument\n
          * By giving real and imaginary part as first two arguments\n
          * By giving explicitely *r=* and *theta=*\n
          * By giving a mathematical expression as the *s* argument\n
        See example below.
        No matter the method you choose, the real and imaginary parts along with norm and argument are set.
        If you modify any of those, the other 3 will be modified accordingly.

        Parameters
        ----------
        a: Optional[Union[float, "Complex"]]
            Real part
        b: Optional[float]
            Imaginary part
        r: Optional[float]
            Norm
        theta: Optional[float]
            Argument
        s: Optional[str]
            String representation
        z: Optional[Complex]
            Another complex number to copy

        Examples
        --------
        >>> znumber = Complex(3, 4)
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(3, 4, 5, 0.9)
        Traceback (most recent call last):
          ...
        ValueError: You specified both cartesian and trigo representations but the values are not compatible
        >>> znumber = Complex(3, 4, 5, 0.9272952180016123)

        >>> znumber = Complex(r=5, theta=0.9272952180016123)
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(s="3+4i")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(s="3")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        0.0
        >>> print(znumber.r)
        3.0
        >>> print(znumber.theta)
        0.0

        >>> znumber = Complex(s="4i")
        >>> print(znumber.a)
        0.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        4.0
        >>> print(znumber.theta)
        1.5707963267948966

        >>> znumber = Complex(s="3cos(0)")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        0.0
        >>> print(znumber.r)
        3.0
        >>> print(znumber.theta)
        0.0

        >>> znumber = Complex(s="4isin(1.5707963267948966)")
        >>> print(znumber.a)
        0.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        4.0
        >>> print(znumber.theta)
        1.5707963267948966

        >>> # In case your string can not be a complex (here we would have two different r for instance),
        >>> # it is the part in 'cos' that is used.
        >>> znumber = Complex(s="3cos(4) + 4isin(1)")
        >>> print(znumber.a)
        -1.960930862590836
        >>> print(znumber.b)
        -2.2704074859237844
        >>> print(znumber.r)
        3.0
        >>> print(znumber.theta)
        4.0

        >>> znumber = Complex(s="3 + 4 * i")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(s="5e^0.9272952180016123i")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber = Complex(s="5*(cos(0.9272952180016123i) + isin(0.9272952180016123i)")
        >>> print(znumber.a)
        3.0
        >>> print(znumber.b)
        4.0
        >>> print(znumber.r)
        5.0
        >>> print(znumber.theta)
        0.9272952180016123

        >>> znumber_2 = Complex(z=znumber)
        >>> print(znumber_2.a)
        3.0
        >>> print(znumber_2.b)
        4.0
        >>> print(znumber_2.r)
        5.0
        >>> print(znumber_2.theta)
        0.9272952180016123

        >>> znumber_2 = Complex(znumber)
        >>> print(znumber_2.a)
        3.0
        >>> print(znumber_2.b)
        4.0
        >>> print(znumber_2.r)
        5.0
        >>> print(znumber_2.theta)
        0.9272952180016123
        """

        if isinstance(a, Complex):
            z = a
            a = None
            b = None
            r = None
            theta = None

        if r is not None and r < 0:
            raise ValueError("A complex number's norm cannot be negative!")

        self.__a = float(a) if a is not None else None
        self.__b = float(b) if b is not None else None
        self.__r = float(r) if r is not None else None
        self.__theta = float(theta) if theta is not None else None

        if z:
            self.a = z.a
            self.b = z.b
            self.r = z.r
            self.theta = z.theta
        elif s:
            self._guess_repr_from_string(s)
        else:
            self._guess_repr()

    @property
    def conjugate(self, repres: str = "cartesian") -> "Complex":
        """Returns the complex conjugate of this complex number

        Parameters
        ----------
        repres: str
            Can be "cartesion" (will use real part and minus imaginary part to create the conjugate), "exp" or "trigo"
             (will use norm and minus the argument to create the conjugate)

        Returns
        -------
        Complex
        """
        if repres == "cartesian":
            return Complex(self.a, -self.b)
        elif repres == "trigo" or repres == "exp":
            return Complex(r=self.r, theta=-self.theta)
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_repr()

    def to_string(self, repres: str = "cartesian") -> str:
        """ Human-readable str

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
        """
        bsign = "+" if self.b > 0 else "-"
        if repres == "cartesian":
            return f"{self.a} {bsign} {abs(self.b)}i"
        elif repres == "trigo":
            return f"{self.r} * (cos({self.theta}) + isin({self.theta}))"
        elif repres == "exp":
            return f"{self.r}e^{self.theta}i"
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def to_repr(self, repres: str = "cartesian") -> str:
        """ str readable by exec() or eval()

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
        """
        bsign = "+" if self.b > 0 else "-"
        if repres == "cartesian":
            return f"{self.a} {bsign} {abs(self.b)} * i"
        elif repres == "trigo":
            return f"{self.r} * (cos({self.theta}) + i * sin({self.theta}))"
        elif repres == "exp":
            return f"{self.r} * e ** ({self.theta} * i)"
        else:
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

        """
        if repres == "cartesian":
            return f"${self.a} + {self.b}i$"
        elif repres == "trigo":
            return f"${self.r} \\times (\\cos({self.theta}) + i \\sin({self.theta}))$"
        elif repres == "exp":
            return f"${self.r} \\text{{e}}^{{{self.theta} i}}$"
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def round(self, n: int, repres: str = "cartesian") -> "Complex":
        """Returns another complex number with rounded attributes using builting `round` method.

        Parameters
        ----------
        n: int
            *n* argument of the *round* method
        repres: str
            Can be "cartesion" (will round real and imaginary parts), "exp" or "trigo" (will round norm and argument)

        Returns
        -------
        Complex

        Examples
        --------
        >>> znumber = Complex(3.123456, 4.789101112)
        >>> print(znumber.round(n=2))
        3.12 + 4.79i
        >>> print((znumber.round(n=2, repres="exp")).to_string("exp"))
        5.72e^0.99i

        """
        if repres == "cartesian":
            return Complex(round(self.a, n), round(self.b, n))
        elif repres == "trigo" or repres == "exp":
            return Complex(r=round(self.r, n), theta=round(self.theta, n))
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def ceil(self, repres: str = "cartesian") -> "Complex":
        """Use `math.ceil` method to create a new complex number

        Parameters
        ----------
        repres: str
            Can be "cartesion" (will ceil real and imaginary parts), "exp" or "trigo" (will ceil norm and argument)

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
        if repres == "cartesian":
            return Complex(math.ceil(self.a), math.ceil(self.b))
        elif repres == "trigo" or repres == "exp":
            return Complex(r=math.ceil(self.r), theta=math.ceil(self.theta))
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def floor(self, repres: str = "cartesian") -> "Complex":
        """Use `math.floor` method to create a new complex number

        Parameters
        ----------
        repres: str
            Can be "cartesion" (will floor real and imaginary parts), "exp" or "trigo" (will floor norm and argument)

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
        if repres == "cartesian":
            return Complex(math.floor(self.a), math.floor(self.b))
        elif repres == "trigo" or repres == "exp":
            return Complex(r=math.floor(self.r), theta=math.floor(self.theta))
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

    def trunc(self, repres: str = "cartesian") -> "Complex":
        """Use `math.trunc` method to create a new complex number

        Parameters
        ----------
        repres: str
            Can be "cartesion" (will truncate real and imaginary parts), "exp" or "trigo"
            (will truncate norm and argument)

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
        if repres == "cartesian":
            return Complex(math.trunc(self.a), math.trunc(self.b))
        elif repres == "trigo" or repres == "exp":
            return Complex(r=math.trunc(self.r), theta=math.trunc(self.theta))
        else:
            raise ValueError(f"Unknown representation {repres}. Possibilities are 'cartesian', 'trigo' or 'expo'")

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
                pd.DataFrame(columns=["$\\mathbb{R}$", "$\\mathbb{C}$"], data=[[self.a, self.b]]),
                x="$\\mathbb{R}$",
                y="$\\mathbb{C}$",
                **kwargs,
            )
        else:
            fig.add_trace(go.Scatter(x=[self.a], y=[self.b], mode="markers", **kwargs))
        return fig

    @property
    def a(self) -> float:
        """Real part.

        If modified, recomputes norm and argument by using `complex.Complex.r_theta_from_ab`
        """
        if str(self.__a) == "-0.0":
            return 0.0
        return self.__a

    @a.setter
    def a(self, value) -> None:
        self.__a = value
        if self.a is None or self.b is None:
            self.__r = None
            self.__theta = None
        else:
            self.__r, self.__theta = r_theta_from_ab(self.a, self.b)

    @property
    def b(self) -> float:
        """Imaginary part.

        If modified, recomputes norm and argument by using `complex.Complex.r_theta_from_ab`
        """
        if str(self.__b) == "-0.0":
            return 0.0
        return self.__b

    @b.setter
    def b(self, value) -> None:
        self.__b = value
        if self.a is None or self.b is None:
            self.__r = None
            self.__theta = None
        else:
            self.__r, self.__theta = r_theta_from_ab(self.a, self.b)

    @property
    def r(self) -> float:
        """Norm.

        If modified, recomputes real and imaginary parts by using `complex.Complex.ab_from_r_theta`
        """
        if str(self.__r) == "-0.0":
            return 0.0
        return self.__r

    @r.setter
    def r(self, value) -> None:
        self.__r = value
        if self.r is None or self.theta is None:
            self.__a = None
            self.__b = None
        else:
            self.__a, self.__b = ab_from_r_theta(self.r, self.theta)

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
        if self.r is None or self.theta is None:
            self.__a = None
            self.__b = None
        else:
            self.__a, self.__b = ab_from_r_theta(self.r, self.theta)

    # Comparison

    def __eq__(self, other: Union[int, float, "Complex", str]) -> bool:
        """

        Example
        -------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(r=5, theta=0.9272952180016123)
        >>> znumber == znumber2
        True

        """
        if isinstance(other, str):
            other = Complex(s=other)
        if isinstance(other, Complex):
            if self.a == other.a and self.b == other.b:
                return True
            if self.r == other.r and self.theta == other.theta:
                return True
        elif self.a == other:
            return True
        return False

    def __ne__(self, other: Union[int, float, "Complex", str]) -> bool:
        """

        Example
        -------
        >>> znumber = Complex(3, 4)
        >>> znumber2 = Complex(r=5, theta=0.9272952180016123)
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
        return Complex(a=-self.a, b=-self.b)

    def __abs__(self) -> float:
        return self.r

    def __round__(self, n: int = 0) -> "Complex":
        return self.round(n=n)

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
            other = Complex(s=other)
        if isinstance(other, Complex):
            new.a = new.a + other.a
            new.b = new.b + other.b
        else:
            new.a = new.a + other
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
            other = Complex(s=other)
        if isinstance(other, Complex):
            new.a = new.a - other.a
            new.b = new.b - other.b
        else:
            new.a = new.a - other
        return new

    def __mul__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber2 = Complex(r=5, theta=6)
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
            other = Complex(s=other)
        if isinstance(other, Complex):
            new.r = new.r * other.r
            new.theta = new.theta + other.theta
        else:
            new.r = new.r * other
        return new

    def __truediv__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber2 = Complex(r=5, theta=6)
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
            other = Complex(s=other)
        if isinstance(other, Complex):
            new.r = new.r / other.r
            new.theta = new.theta - other.theta
        else:
            new.r = new.r / other
        return new

    def __pow__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber2 = Complex(r=5, theta=6)
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

        if isinstance(other, str) or isinstance(other, Complex):
            return NotImplemented
        new.r = new.r ** other
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
        return self.conjugate * other / self.r ** 2

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
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber *= Complex(r=5, theta=6)
        >>> print(znumber.to_string("exp"))
        15.0e^10.0i

        """
        return self * other

    def __idiv__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber /= Complex(r=5, theta=6)
        >>> print(znumber.to_string("exp"))
        0.6e^-2.0i

        """
        return self / other

    def __ipow__(self, other: Union[int, float, "Complex", str]) -> "Complex":
        """

        Examples
        --------
        >>> znumber = Complex(r=3, theta=4)
        >>> znumber **= Complex(r=5, theta=6)
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
        return Complex(z=self)

    def __setattr__(self, key, value):
        """

        Examples
        --------
        >>> z = Complex(3, 4)
        >>> z.r
        5.0
        >>> z.q = 2
        Traceback (most recent call last):
        ...
        complex.ForbiddenAssignmentError: The Complex class does not allow for new attributes assignment
        >>> z.a = 4
        >>> z.r
        5.656854249492381
        >>> z.__r = 4
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
        cartesian = False
        trigo = False

        if self.__a is not None and self.__b is not None:
            cartesian = True
        if self.__r is not None and self.__theta is not None:
            trigo = True
        if not cartesian and not trigo:
            raise ValueError("Not enough information provided at Complex number creation.")

        if cartesian:
            if self.__a is None or self.__b is None:
                r = None
                theta = None
            else:
                r, theta = r_theta_from_ab(self.__a, self.__b)
            if trigo:
                # Do not set self.r and self.theta if trigo representation was found, since they were already specified
                # by the user. Just check that those values are compatible with the given a and b
                if not compatible_numbers(r, self.__r) or not compatible_numbers(theta, self.__theta):
                    raise ValueError(
                        "You specified both cartesian and trigo representations but the values are not compatible"
                    )
            else:
                self.a = self.__a
                self.b = self.__b
        # If trigo, then not cartesian too. Set a and b.
        else:
            self.r = self.__r
            self.theta = self.__theta

    def _guess_repr_from_string(self, s) -> None:
        """Same as `complex.Complex._guess_repr` but using a string as input"""
        s = s.replace("(", "")
        s = s.replace(")", "")
        s = s.replace("*", "")
        s = s.replace("x", "")
        s = s.replace(" ", "")
        # TODO (pcotte) Add possibility to write something like '3 x e^(i x pi / 4)'
        if "e^" in s or "exp" in s:
            s = s.replace("i", "")
            if "e^" in s:
                self.r = float(s.split("e^")[0])
                self.theta = float(s.split("e^")[1])
            else:
                self.r = float(s.split("exp")[0])
                self.theta = float(s.split("exp")[1])
        elif "cos" in s or "sin" in s:
            ss = s.split("+")[0].replace("i", "")
            if "cos" in ss:
                self.r = float(ss.split("cos")[0])
                self.theta = float(ss.split("cos")[1])
            else:
                self.r = float(ss.split("sn")[0])
                self.theta = float(ss.split("sn")[1])
        else:
            if "+" not in s:
                if "i" in s:
                    self.a = 0.0
                    self.b = float(s.replace("i", ""))
                else:
                    self.a = float(s)
                    self.b = 0.0
            else:
                self.a = float(s.split("+")[0].replace(" ", ""))
                self.b = float(s.split("+")[1].replace(" ", "").replace("i", ""))


i = Complex(0, 1)
"""The pure imaginary number"""

mathexp = math.exp


def myexp(x) -> Union[float, Complex]:
    """Overloads `math.exp` to accept complex numbers"""
    if isinstance(x, Complex):
        return mathexp(x.a) * Complex(r=1, theta=x.b)
    else:
        return mathexp(x)


math.exp = myexp

mathlog = math.log


def mylog(x: Union[SupportsFloat, Complex], base=None) -> Union[float, Complex]:
    """Overloads `math.log` to accept complex numbers"""
    if isinstance(x, Complex):
        if base is None:
            return mathlog(x.r) + i * x.theta
        else:
            return mathlog(x.r, base) + i * x.theta / mathlog(base)
    else:
        print(x)
        if base is None:
            return mathlog(x)
        else:
            return mathlog(x, base)


math.log = mylog
