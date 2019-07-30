#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/22.
"""

import os

from setuptools import find_packages, setup


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='ruia_pyppeteer',
    version='0.0.5',
    author='Howie Hu',
    description="ruia_pyppeteer - A Ruia plugin for loading javascript - pyppeteer.",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author_email='xiaozizayang@gmail.com',
    install_requires=['ruia>=0.6.1', 'pyppeteer'],
    url="https://github.com/ruia-plugins/ruia-pyppeteer",
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Documentation': 'https://github.com/python-ruia/ruia-pyppeteer',
        'Source': 'https://github.com/python-ruia/ruia-pyppeteer',
    }
)
