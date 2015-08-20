#!/usr/bin/env python

import os
import graphql

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

packages = ['graphql']
requires = ['ply>=3.6']

setup(
    name='graphql-py',
    version=graphql.__version__,
    description='graphql-py: Parser for latest GraphQL specification',
    long_description=open('README.rst').read(),
    author='Denis Stebunov',
    author_email='support@ivelum.com',
    url='https://github.com/ivelum/graphql-py/',
    packages=packages,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ),
)

del os.environ['PYTHONDONTWRITEBYTECODE']