#!/usr/bin/env python3
# coding=utf-8

import os
from setuptools import setup
from glob import glob

version = "1.2.1"


setup(
    name='jutge-problems-toolkit',
    packages=['jutge_problems_toolkit'],
    install_requires=['pyyaml'],
    version=version,
    description='Toolkit to create problems for Jutge.org',
    long_description='Toolkit to create problems for Jutge.org',
    author='Jordi Petit et al',
    author_email='jpetit@cs.upc.edu',
    url='https://github.com/jutge-org/jutge-problems-toolkit',
    download_url='https://github.com/jutge-org/jutge-problems-toolkit/tarball/{}'.format(version),
    keywords=['jutge', 'jutge.org', 'education', 'problems', 'toolkit'],
    license='Apache',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Education',
    ],
    zip_safe=False,
    include_package_data=True,
    setup_requires=['setuptools'],
    entry_points={'console_scripts': ['jutge-problems-toolkit=jutge_problems_toolkit:main']}
)

print(os.path.abspath(__file__))
