#!/usr/bin/env python

from os import path as op

from setuptools import setup, find_packages


def _read(fname):
    try:
        return open(op.join(op.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name='sanic-oauth',
    version='0.2.0',
    license='MIT',
    long_description=_read('README.rst'),
    keywords=['asyncio', 'http', 'oauth', 'sanic'],
    author='Gladyshev Bogdan',
    packages=find_packages(),
    author_email='siredvin.dark@gmail.com',
    url='https://gitlab.com/SirEdvin/sanic-oauth',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    install_requires=[
        "yarl >= 1.1.0",
        "aiohttp >= 2.3.9"
    ],
)
