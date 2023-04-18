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
    version='0.5.0',
    license='MIT',
    long_description=_read('README.rst'),
    keywords=['asyncio', 'http', 'oauth', 'sanic'],
    author='hamed sh',
    packages=find_packages(),
    author_email='hamed.sheykhlu@gmail.com',
    url='https://gitlab.com/hamedsh/sanic-oauth',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Framework :: AsyncIO',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    install_requires=[
        "yarl~=1.8.2",
        "aiohttp~=3.8.4"
    ],
)
