"""
This is the setup module for the opcu project.

Based on:

- https://packaging.python.org/distributing/
- https://github.com/pypa/sampleproject/blob/master/setup.py
- https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
"""

from glob import glob
from os.path import splitext, basename

from setuptools import setup, find_packages


def readme():
    """Read in and return the contents of the project's README.md file."""
    with open("README.md") as f:
        return f.read()


def package_vars(version_file):
    """Read in and return the variables defined by the version_file."""
    pkg_vars = {}
    with open(version_file) as f:
        exec(f.read(), pkg_vars)  # nosec
    return pkg_vars


setup(
    name="opcu",
    # Versions should comply with PEP440
    version=package_vars("src/opc/_version.py")["__version__"],
    description="Multi Open Pixel Controller over UDP",
    long_description=readme(),
    long_description_content_type="text/markdown",
    # Geekpad
    url="https://geekpad.com",
    # The project's main homepage
    download_url="https://github.com/felddy/opcu",
    # Author details
    author="Mark Feldhousen",
    author_email="markf+opcu@geekpad.com",
    license="License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # What does your project relate to?
    keywords="pixel led udp control",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=["docopt >= 0.6.2", "PyYAML >= 3.12", "watchdog >= 0.8.3"],
    extras_require={"test": ["pre-commit", "pytest", "pytest-cov", "coveralls"]},
    entry_points={"console_scripts": ["multi-opc = opc.multi_opc:main"]},
)
