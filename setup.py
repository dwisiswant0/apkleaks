#!/usr/bin/env python3
from setuptools import setup

install_requires = open('requirements.txt', 'r').readlines()
version = open('VERSION', 'r').read().strip()

setup(
    name='apkleaks',
    version=version,
    packages=['apkleaks'],
    url='https://github.com/dwisiswant0/apkleaks/',
    license='Apache License 2.0',
    author='dwisiswant0',
    author_email='me@dw1.io',
    description='Scanning APK file for URIs, endpoints & secrets.',
    install_requires=install_requires,
    scripts=['apkleaks.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Topic :: Security',
        'Topic :: Utilities',
    ]
)
