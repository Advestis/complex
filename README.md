[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/complex)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
[![pytests](https://github.com/Advestis/complex/actions/workflows/pull-request.yml/badge.svg)](https://github.com/Advestis/complex/actions/workflows/pull-request.yml)
[![push](https://github.com/Advestis/complex/actions/workflows/push.yml/badge.svg)](https://github.com/Advestis/complex/actions/workflows/push.yml)

![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
[![issues](https://img.shields.io/github/issues/Advestis/complex.svg)](https://github.com/Advestis/complex/issues)
[![pr](https://img.shields.io/github/issues-pr/Advestis/complex.svg)](https://github.com/Advestis/complex/pulls)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/pypi/pyversions/complex)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-Advestis-blue)](https://www.linkedin.com/company/advestis/)
[![website](https://img.shields.io/badge/website-Advestis.com-blue)](https://www.advestis.com/)
[![mail](https://img.shields.io/badge/mail-maintainers-blue)](mailto:pythondev@advestis.com)

# Complex

A class implementing the notion of complex number, used as a template for public packages

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

## Use this package as a template

Make a new public github repository by using this one as template. Clone your new repository, then do

```bash
cd <your_cloned_directory>
rm -rf .git
git init .
rm .gitattributes
rm versioneer.py
rm complex/_version.py
```

Then change the following directory names:
* [complex](complex) -> your project name without upper case

Then change the following files:
* [setup.cfg](setup.cfg): search and replace **complex** with your new project name (no upper case!!). Change the project
description, author and author email. Change the 'install_requires' session, by filling it with what used to be the
*requirements.txt* file
* [MANIFEST.in](MANIFEST.in) : delete the line **include complex/_version.py**
* [tests/conftest.py](tests/conftest.py) : delete if not needed
* [tests/test_complex.py](tests/test_complex.py) : -> rename the file and empty the file
* [complex/\_\_init\_\_.py](complex/__init__.py) : empty the file
* [complex/complex.py](complex/complex.py) : rename and empty the file
* [.github/workflows/push.yml](.github/workflows/push.yml) : uncomment the end of the file (step *topypi*)
* [README.md](README.md) : change the occurences of **complex** in the urls at the top of the file, and change the
rest of the file content to describe your poject.
* Install and use **versioneer** (see below)
* push to master
* Protect your master branch (in github repository's settings)
* Make a new branch locally, push and make a PR to master to check that the CI/CD triggers your pytests.
* Set the GitHub pages of your repo

## Use versioneer in your package

In you project directory, with a loaded virtualenv, do :
* `pip install versioneer`
* `versioneer install`
* commit the new files
* Verify version information with `python setup.py version`
