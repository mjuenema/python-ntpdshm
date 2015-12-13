#!/usr/bin/env python
# -*- coding: utf-8 -*-


#try:
from setuptools import setup, Extension
#except ImportError:
#from distutils.core import setup, Extension


ntpdshm_module = Extension('_ntpdshm', sources=['ntpdshm/ntpdshm.i'],)


from os.path import join, dirname


from ntpdshm import NAME, VERSION, LICENSE, AUTHOR, EMAIL, DESCRIPTION, URL

readme = open(join(dirname(__file__), 'README.rst')).read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # 'package1', 'package2'
    
]

test_requirements = [
    # 'package1', 'package2'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme + '\n\n' + history,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=[
        NAME,
    ],
    package_dir={'ntpdshm':
                 'ntpdshm'},
    include_package_data=True,
    install_requires=requirements,
    ext_modules = [ntpdshm_module],
    py_modules = ['ntpdshm'],
    license=LICENSE,
    zip_safe=False,
    keywords='ntp, shared memory',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
