from setuptools import setup, find_packages

setup(
    name="syngrep",
    version="0.0.4",
    packages=["syngrep"],
    author_email="takdavid@gmail.com",
    scripts=["scripts/syngrep"],
    install_requires=["nltk", "more_itertools"]
)
