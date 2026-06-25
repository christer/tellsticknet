#!/usr/bin/env python

from setuptools import setup, find_packages
from os.path import exists


setup(
    name="tellsticknet",
    version="0.1.2",
    description="Listen for UDP sensor broadcasts from a Tellstick",
    url="https://github.com/molobrakos/tellsticknet",
    license="?",
    author="Erik Eriksson",
    author_email="error.errorsson@gmail.com",
    keywords="tellstick",
    packages=find_packages(),
    long_description=(open("README.md").read() if exists("README.md") else ""),
    scripts=[],
    extras_require={},
    python_requires=">=3.14",
    zip_safe=False,
)
