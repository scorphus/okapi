import sys

from setuptools import find_packages

setup(
    name='okapi',
    version='0.1',
    author='RedBeacon',
    description='Python Library to send API info to Storage Server',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)