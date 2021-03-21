#!/usr/bin/env python3
from setuptools import setup, find_packages

install_requires = open('./requirements.txt', 'r').readlines()
version = open('./VERSION', 'r').read().strip()
packages = find_packages(exclude=['*.tests', '*.tests.*', 'test*', 'tests'])
packages.append('config')

setup(
    name='apkleaks',
    version=version,
    packages=packages,
    url='https://github.com/dwisiswant0/apkleaks/',
    license='Apache License 2.0',
    author='dwisiswant0',
    author_email='me@dw1.io',
    description='Scanning APK file for URIs, endpoints & secrets.',
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "apkleaks=apkleaks.cli:main",
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Topic :: Security',
        'Topic :: Utilities',
    ]
)
