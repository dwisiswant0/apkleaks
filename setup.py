from setuptools import setup

install_requires = open('requirements.txt', 'r').readlines()

setup(
    name='apkleaks',
    version='2.0.8',
    packages=['apkleaks'],
    url='https://github.com/dwisiswant0/apkleaks/',
    license='Apache License 2.0',
    author='dwisiswant0',
    author_email='',
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
