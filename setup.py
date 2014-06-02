import os
import sys
import requests

from setuptools import find_packages
from setuptools import setup

setup(
    name='okapi',
    version='0.1',
    author='RedBeacon',
    description='Python Library to send API info to Storage Server',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    install_requires = [
        'pymongo',
        'mongo',
        'requests',
    ],

)