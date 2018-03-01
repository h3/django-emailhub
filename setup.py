# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

VERSION = '0.0.1'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='emailhub',
    version=VERSION,
    description='Yet another email management app for django',
    long_description=(read('README.md')),
    author='Maxime Haineault',
    author_email='haineault@gmail.com',
    license='MIT',
    url='https://github.com/h3/django-emailhub',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'django-multi-email-field==0.5.1',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
