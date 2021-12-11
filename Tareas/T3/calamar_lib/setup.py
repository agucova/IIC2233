from setuptools import setup, find_packages

setup(
    name="calamar_lib",
    description="Common utilities for the client and server of DCCalamar",
    version="0.1.0",
    packages=find_packages(include=["calamarlib"]),
)
