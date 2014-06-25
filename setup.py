# Copyright 2014 Red Beacon, Inc.  All Rights Reserved
#
# This code, and all derivative work, is the exclusive property of
# Red Beacon, Inc. and may not be used without Red Beacon, Inc.'s
# authorization.
#
# Author: Gobind Ball

from setuptools import find_packages
from setuptools import setup

setup(
    name='okapi',
    version='0.5',
    author='RedBeacon (Gobind Ball)',
    author_email='support@redbeacon.com',
    description='Python Library to send API info to Storage Server',
    packages=find_packages(),
    data_files=[('config',['setup.cfg'])],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    install_requires = [
        'pymongo',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'okapi=okapi:mongo',
        ],
    },
)