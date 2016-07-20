from setuptools import setup, find_packages

setup(
    name="Synonym grep",
    version="0.0.1",
    packages=find_packages(),
    author_email="takdavid@gmail.com",
    install_requires=["nltk", "more_itertools"]
)
