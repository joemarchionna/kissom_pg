import setuptools
from setuptools import setup

setup(
    name="kissom_pg",
    version="1.5.0",
    author="Joe Marchionna",
    author_email="joemarchionna@gmail.com",
    description="Keep It Simple Stupid Object Manager - PostgreSQL Adapter",
    long_description=open("readme.md").read(),
    license=open("license.md").read(),
    packages=setuptools.find_packages(),
    url="https://github.com/joemarchionna/kissom_pg.git",
    keywords=["PostgreSQL", "ADAPTER", "ORM"],
    install_requires=open("requirements/prod.txt", "r").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
