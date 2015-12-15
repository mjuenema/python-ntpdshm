# -*- coding: utf-8 -*-

NAME = 'ntpdshm'
VERSION = '0.1.0'
LICENSE = 'BSD License'
AUTHOR = 'Markus Juenemann'
EMAIL = 'markus@juenemann.net'
DESCRIPTION = 'Python interface to NTP Shared Memory'
URL = 'https://github.com/mjuenema/python-ntpdshm'

from setuptools import setup, Extension
ntpdshm_module = Extension('ntpdshm._shm', sources=['ntpdshm/shm.c', 'ntpdshm/shm_wrap.c'],)

from os.path import join, dirname

readme = open(join(dirname(__file__), 'README.rst')).read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open(join(dirname(__file__), 'requirements.txt')).read().split()
test_requirements = open(join(dirname(__file__), 'test_requirements.txt')).read().split()

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
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Networking :: Time Synchronization',
        'Programming Language :: Python :: C',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
