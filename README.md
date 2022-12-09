[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/complex)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
[![pytests](https://github.com/Advestis/complex/actions/workflows/pull-request.yml/badge.svg)](https://github.com/Advestis/complex/actions/workflows/pull-request.yml)
[![push-pypi](https://github.com/Advestis/complex/actions/workflows/push-pypi.yml/badge.svg)](https://github.com/Advestis/complex/actions/workflows/push-pypi.yml)
[![push-doc](https://github.com/Advestis/complex/actions/workflows/push-doc.yml/badge.svg)](https://github.com/Advestis/complex/actions/workflows/push-doc.yml)

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

## Complex

Class implementing the notion of complex number.

This repository serves as a **template for pip-installable public packages**.

### Installation

```
git clone https://github.com/Advestis/complex
cd complex
python setup.py install
```

### Usage

```python
from complex import Complex

znumber = Complex(3, 4)
znumber_fromstring = Complex(from_string="3+4i")
znumber_fromstring_cos = Complex(from_string="3cos(4) + 4isin(1)")
znumber_fromstring_exp = Complex(from_string="5e^3.1415926i")
znumber + znumber_fromstring
z_conj = znumber.conjugate
```

### Use this package as a template

To make a pip-installable public Python package, follow the instructions below.

1. Make a new blank public GitHub repository, naming it as you want.


2. Clone **complex** locally, open a terminal and execute the following lines

```bash
cd <parent directory of the cloned complex repo>
mv complex <your_new_repo_name>
cd <your_new_repo_name>
rm -rf .git
git init .
rm .gitattributes
rm versioneer.py
rm complex/_version.py
git remote add origin https://github.com/your_new_repo_name
```

3. Rename the project subfolder in `<your_new_repo_name>`
   * [complex](complex) ---> your project name (no uppercase!)


4. **Modify project configuration files**
   * [setup.cfg](setup.cfg) :
     - Search and replace the occurences of "**complex**" with your new project name (no uppercase!)
     - Change the project description, author and author email
     - In `[options]` section, fill the contents of `install_requires` parameter from
       with what you normally put in your *requirements.txt* file
       (do not forget the indentation!) **This is important**, as otherwise your PyPI package will not include
       neither automatically install other required packages.
   * [MANIFEST.in](MANIFEST.in) : Delete the line `include complex/_version.py`
   * [tests/conftest.py](tests/conftest.py) : Delete if not needed
   * [tests/test_complex.py](tests/test_complex.py) : Rename and empty the file
   * [complex/\_\_init\_\_.py](complex/__init__.py) : Empty the file
   * [complex/complex.py](complex/complex.py) : Rename and empty the file
   * [.github/workflows/push-pypi.yml](.github/workflows/push-pypi.yml) : Uncomment the end of the file (*topypi* step)
   * [README.md](README.md) :
     - Change the occurences of "**complex**" in the URLs at the top of the file
     - Change the rest of the file content to describe your project


5. **Install and use VERSIONEER**
   * In you project directory, with a loaded virtualenv, execute :
   ```bash
   pip install versioneer
   versioneer install
   git tag v0.1
   ```
   * Add the line `include you_package_name/_version.py` to [MANIFEST.in](MANIFEST.in)
   * Commit your modified files
   * Verify version information with `python setup.py version`. The version should be "v0.1"


6. Push to `master`, including tags : at the bottom of PyCharm's push window, check the checkbox *push tags*.
   If using the command line, do `git push -u origin master --follow-tags`


7. Protect your `master` branch in GitHub repository's settings, according to your needs.


8. Make a new branch locally, push and make a PR to `master` to check that the CI/CD will trigger your pytests.


9. Set [GitHub pages](https://pages.github.com/) of your repo, if you'd like.


10. **Manage your public package** (repeat according to your needs)
    * Working on a local branch, fill the project subfolder with your code and modify `__init__.py` file in it 
    as you wish.
    * Push and make a PR to `master`, then approve it (with assigned reviewers if required).
    * Merging this PR will update your public package on PyPI, putting a new subversion (0.1.1 ---> 0.1.2 etc.)
