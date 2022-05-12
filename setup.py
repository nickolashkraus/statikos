#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script."""

from setuptools import find_packages, setup

description = \
    'A Python package for generating static websites using AWS CloudFormation.'

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().split()

with open('requirements_dev.txt') as requirements_dev_file:
    requirements_dev = requirements_dev_file.read().split()
    requirements_dev = list(filter(lambda x: '==' in x, requirements_dev))

install_requirements = requirements

setup_requirements = []

test_requirements = requirements_dev

setup(
    author='Nickolas Kraus',
    author_email='0x@nickolaskraus.io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English', 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    description=description,
    entry_points={
        'console_scripts': ['statikos=statikos.cli:cli', ],
    },
    install_requires=install_requirements,
    license='MIT License',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='statikos',
    name='statikos',
    packages=find_packages(include=['statikos']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/NickolasHKraus/statikos',
    version='0.1.0',
    zip_safe=False,
)
