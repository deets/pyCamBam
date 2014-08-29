import sys
from setuptools import setup, find_packages

setup(
    name = "pyCamBam",
    version = "1.0",
    packages = find_packages(),
    install_requires = [],
    author = "Diez B. Roggisch",
    author_email = "deets@web.de",
    description = "A small utility package to create CamBam(tm) project files ",
    license = "GPL",
    classifiers = [
      "Development Status :: 3 - Alpha",
      "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
      "Programming Language :: Python :: 2.7",
      "Intended Audience :: Developers",
    ],
)
