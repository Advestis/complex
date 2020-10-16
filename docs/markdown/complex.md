# complex package

## Module contents


### class complex.Complex(a: Union[float, Complex] = None, b: float = None, r: float = None, theta: float = None, s: str = None, z: Optional[complex.Complex] = None)
Bases: `object`


#### property a()

#### property arg()
### Examples

```python
>>> z = Complex(3, 4)
>>> print(z.arg)
0.9272952180016123
>>> z = Complex(r=2, theta=5)
>>> print(z.arg)
5.0
```


#### property b()

#### ceil(repres: str = 'cartesian')
### Examples

```python
>>> znumber = Complex(3.123456, 4.789101112)
>>> print(znumber.ceil())
4.0 + 5.0i
>>> print((znumber.ceil(repres="exp")).to_string("exp"))
6.0e^1.0i
```


#### property conjugate()

#### floor(repres: str = 'cartesian')
### Examples

```python
>>> znumber = Complex(3.123456, 4.789101112)
>>> print(znumber.floor())
3.0 + 4.0i
>>> print((znumber.floor(repres="exp")).to_string("exp"))
5.0e^0.0i
```


#### property mod()
### Examples

```python
>>> z = Complex(3, 4)
>>> print(z.mod)
5.0
>>> z = Complex(r=2, theta=5)
>>> print(z.mod)
2.0
```


#### plot(fig: plotly.graph_objs._figure.Figure = None, \*\*kwargs)

#### property r()

#### round(n: int, repres: str = 'cartesian')
### Examples

```python
>>> znumber = Complex(3.123456, 4.789101112)
>>> print(znumber.round(n=2))
3.12 + 4.79i
>>> print((znumber.round(n=2, repres="exp")).to_string("exp"))
5.72e^0.99i
```


#### property theta()

#### to_latex(repres: str = 'cartesian')
### Examples

```python
>>> z = Complex(3, 3)
>>> print(z.to_latex())
$3.0 + 3.0i$
>>> print(z.to_latex("trigo"))
$4.242640687119285 \times (\cos(0.7853981633974483) + i \sin(0.7853981633974483))$
>>> print(z.to_latex("exp"))
4.242640687119285 \text{e}^{0.7853981633974483 i}
```


#### to_repr(repres: str = 'cartesian')
### Examples

```python
>>> z = Complex(3, 3)
>>> print(repr(z))
3.0 + 3.0 * i
>>> print(z.to_repr("trigo"))
4.242640687119285 * (cos(0.7853981633974483) + i * sin(0.7853981633974483))
>>> print(z.to_repr("exp"))
4.242640687119285 * e ** (0.7853981633974483 * i)
```


#### to_string(repres: str = 'cartesian')
### Examples

```python
>>> z = Complex(3, 3)
>>> print(z)
3.0 + 3.0i
>>> print(z.to_string("trigo"))
4.242640687119285 * (cos(0.7853981633974483) + isin(0.7853981633974483))
>>> print(z.to_string("exp"))
4.242640687119285e^0.7853981633974483i
```


#### trunc(repres: str = 'cartesian')
### Examples

```python
>>> znumber = Complex(3.123456, 4.789101112)
>>> print(znumber.trunc())
3.0 + 4.0i
>>> print((znumber.trunc(repres="exp")).to_string("exp"))
5.0e^0.0i
```


### exception complex.ForbiddenAssignmentError()
Bases: `Exception`


### complex.ab_from_r_theta(r: [<class 'float'>, None], theta: [<class 'float'>, None])

### complex.compatible_numbers(n1: float, n2: float, threshold: float = 1e-08)
Returns True of both numbers are equal or almost the same


### complex.r_theta_from_ab(a: Optional[float], b: [<class 'float'>, None])
