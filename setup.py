# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='generic_wrapper',
    version='0.1.0',
    description='Generic Wrapper',
    long_description=readme,
    author='Laura Rodriguez-Navas',
    author_email='laura.rodriguez@bsc.es',
    url='https://github.com/inab/generic_wrapper.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

