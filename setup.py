from setuptools import setup

NAME = "toxiproxy"
VERSION = "0.1.0"
DESCRIPTION = "Python library for Toxiproxy"
LONG_DESCRIPTION = """\
A Python library for controlling Toxiproxy. Can be used in resiliency testing."""

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Douglas Soares de Andrade",
    author_email="contato@douglasandrade.com",
    url="https://github.com/douglas/toxiproxy-python",
    packages=["toxiproxy"],
    scripts=[],
    license="MIT License",
    install_requires=[
        "future",
        "requests"
    ],
    test_suite="test",
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        "future",
        "requests",
        "pytest",
        "pytest-sugar",
        "pytest-cov"
    ],
    platforms="Any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
