#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def get_info(name):
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'pdfbookmarker.py')) as f:
        locals = {}
        try:
            exec(f.read(), locals)
        except ImportError:
            pass
        return locals[name]


setup(
    name='pdfbookmarker',
    version=get_info('__version__'),
    author=get_info('__author__'),
    author_email=get_info('__email__'),
    maintainer=get_info('__author__'),
    maintainer_email=get_info('__email__'),
    keywords='PDF, Bookmarks, Python tools',
    description='Add bookmarks to existing PDF files',
    license=get_info('__license__'),
    long_description=get_info('__doc__'),
    py_modules=['pdfbookmarker'],
    url='https://github.com/RussellLuo/pdfbookmarker',
    install_requires=[
        'PyPDF2==1.26.0',
    ],
    entry_points={
        'console_scripts': [
            'pdfbm = pdfbookmarker:main',
        ],
    },
)
