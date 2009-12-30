#!/usr/bin/env python
"""
License: BSD

(c) 2009 ::: Robert Corsaro (doki_pen@doki-pen.org)
"""

from setuptools import setup, find_packages

setup(
    name='TracGatePlugin',
    version='0.11',
    license='BSD',
    author='Robert Corsaro',
    author_email='doki_pen@doki-pen.org',
    url='http://github.com/dokipen',
    description='XML-RPC interface to TracGate, the lamson trac email application',
    zip_safe=True,
    packages=find_packages(exclude=['*.tests']),
    package_data={
        'tracrpc': ['templates/*.html']
        },
    entry_points={
        'trac.plugins': [
            'tracgate.api = tracgate.api',
            'tracgate.email_decorator = tracgate.email_decorator',
            'tracgate.xmlrpc = tracgate.xmlrpc',
        ]
    },
)
