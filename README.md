[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/complex)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
![Pytests](https://github.com/Advestis/complex/actions/workflows/pull-request.yml/badge.svg)
![push](https://github.com/Advestis/complex/actions/workflows/push.yml/badge.svg)

![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![issues](https://img.shields.io/github/issues/Advestis/complex.svg)
![pr](https://img.shields.io/github/issues-pr/Advestis/complex.svg)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/pypi/pyversions/complex)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-Advestis-blue)](https://www.linkedin.com/company/advestis/)
[![website](https://img.shields.io/badge/website-Advestis.com-blue)](https://www.advestis.com/)
[![mail](https://img.shields.io/badge/mail-maintainers-blue)](mailto:pythondev@advestis.com)

# Complex

A class implementing the notion of complex number

## Installation

```
git clone https://github.com/pcotteadvestis/Complex
cd Complex
python setup.py install
```

## Usage

```python
from complex import Complex
znumber = Complex(3, 4)
znumber_fromstring = Complex(s="3+4i")
znumber_fromstring_cos = Complex(s="3cos(4) + 4isin(1)")
znumber_fromstring_exp = Complex(s="5e^3.1415926i")
znumber + znumber_fromstring
z_conj = znumber.conjugate
```
