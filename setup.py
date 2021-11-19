import subprocess
from pathlib import Path
from typing import List
import sys

from setuptools import find_packages, setup

workdir = Path(__file__).parent

name = Path(__file__).absolute().parent.stem
author = "Philippe COTTE"
author_email = "pcotte@advestis.com"
description = "A package doing simulated and quantum annealing"
url = f"https://github.com/Advestis/{name}"


def run_cmd(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split(" ")
    return subprocess.check_output(cmd).decode(encoding="UTF-8").split("\n")


def get_greatest_version(versions: List[str]) -> str:
    versions = [list(map(int, v[1:].split("."))) for v in versions]
    greatest = None
    for v in versions:
        if greatest is None:
            greatest = v
        else:
            lower = False
            for i in range(len(v)):
                if len(greatest) < i + 1:
                    greatest = v
                    break
                if v[i] > greatest[i]:
                    greatest = v
                    break
                if v[i] < greatest[i]:
                    lower = True
                    break
            if not lower:
                greatest = v
    return f"v{'.'.join([str(s_) for s_ in greatest])}"


def get_last_tag() -> str:
    result = [v for v in run_cmd("git tag -l v*") if not v == ""]
    if len(result) == 0:
        run_cmd("git tag v0.1")
    result = [v for v in run_cmd("git tag -l v*") if not v == "" and v.startswith("v")]
    return get_greatest_version(result)


def get_nb_commits_until(tag: str) -> int:
    return len(run_cmd(f'git log {tag}..HEAD --oneline'))


def get_version() -> str:
    last_tag = get_last_tag()
    return f"{'.'.join(last_tag.split('.'))}.{get_nb_commits_until(last_tag)}"


git_installed = subprocess.call('command -v git >> /dev/null', shell=True)

try:
    long_description = (workdir / "README.md").read_text()
except UnicodeDecodeError:
    with open(str(workdir / "README.md"), "rb") as ifile:
        lines = [line.decode("utf-8") for line in ifile.readlines()]
        long_description = "".join(lines)

requirements = (workdir / "requirements.txt").read_text().splitlines()

version = None
if git_installed == 0:
    try:
        version = get_version()
        with open(str(workdir / "VERSION.txt"), "w") as vfile:
            vfile.write(version)
    except FileNotFoundError as e:
        pass
if version is None:
    # noinspection PyBroadException
    try:
        with open(str(workdir / "VERSION.txt"), "r") as vfile:
            version = vfile.readline()
    except Exception:
        version = None


if __name__ == "__main__":

    if sys.argv[1] == "version":
        exit(0)

    setup(
        name=name,
        version=version,
        author=author,
        author_email=author_email,
        include_package_data=True,
        description=description,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=url,
        packages=find_packages(),
        install_requires=requirements,
        package_data={"": ["*", ".*"]},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable"
        ],
        python_requires='>=3.7',
    )
