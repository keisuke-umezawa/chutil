import setuptools
import sys
import os
from glob import glob

# hack to extract metadata directly from the python package
sys.path.append("src")  # noqa
from chutil import __author__, __version__, __license__


def read(fname):
    with open(fname, "r", encoding="utf-8") as fh:
        long_description = fh.read()
        return long_description


setuptools.setup(
    name="chutil",
    version=__version__,
    description="Chainer Utilities",
    author=__author__,
    author_email="keisuke.umezawa@gmail.com",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license=__license__,
    url="https://github.com/keisuke-umezawa/chutil.git",
    keywords="",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")
    ],
    install_requires=[],
    tests_require=[
        "pytest-cov>=2.5.1",
        "pytest-mock>=1.7.1",
        "pytest-flake8>=1.0.0",
        "pytest-sugar>=0.9.1",
        "pytest>=3.5.0",
        "autopep8>=1.2.3",
        "flake8>=3.5.0",
    ],
)
