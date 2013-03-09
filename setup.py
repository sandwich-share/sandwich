#!/usr/bin/env python

from setuptools import setup

__version__ = '0.1'

setup(
  name = 'sandwich',
  version = __version__,
  description = 'A little file sharing application.',
  author = 'HacSoc',
  author_email = 'hacsoc@case.edu',
  url = 'https://github.com/hacsoc/hacKSU',
  long_description=open("README").read(),
  install_requires = [
  ],
  license = 'BSD',
  classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
  ]
)
