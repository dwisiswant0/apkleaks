#!/usr/bin/env python3
from os import path
from setuptools import setup, find_packages

main_dir = path.abspath(path.dirname(__file__))
install_requires = open(path.join(main_dir, "requirements.txt"), "r").readlines()
version = open(path.join(main_dir, "VERSION"), "r").read().strip()
long_description = open(path.join(main_dir, "README.md"), "r", encoding="utf-8").read()
packages = find_packages(exclude=["*.tests", "*.tests.*", "test*", "tests"])
packages.append("config")

setup(
    name="apkleaks",
    version=version,
    packages=packages,
    url="https://github.com/dwisiswant0/apkleaks/",
    license="Apache License 2.0",
    author="dwisiswant0",
    author_email="me@dw1.io",
    description="Scanning APK file for URIs, endpoints & secrets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "apkleaks=apkleaks.cli:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Security",
        "Topic :: Utilities",
    ]
)
