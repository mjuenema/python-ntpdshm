


all: help

help:
	exit 1


# ---------------------------------------------------------
#  
#  packaging
#
sdist: clean swig
	python setup.py sdist

bdist: clean swig
	python setup.py bdist

rpm: clean swig
	python setup.py bdist_rpm

upload: clean swig sdist
	twine upload dist/*

info:
	python setup.py egg_info

register:
	echo "https://pypi.python.org/pypi?%3Aaction=submit_form"


# ---------------------------------------------------------
#  
# build
#
build_ext: clean swig
	python setup.py build_ext
	python setup.py build_ext --inplace

build_ext26: clean swig
	python2.6 setup.py build_ext
	python2.6 setup.py build_ext --inplace

build_ext27: clean swig
	python2.7 setup.py build_ext
	python2.7 setup.py build_ext --inplace

build_ext33: clean swig
	python3.3 setup.py build_ext
	python3.3 setup.py build_ext --inplace

build_ext34: clean swig
	python3.4 setup.py build_ext
	python3.4 setup.py build_ext --inplace

build_ext35: clean swig
	python3.5 setup.py build_ext
	python3.5 setup.py build_ext --inplace

swig: clean
	( cd ntpdshm ; swig -python shm.i )

# ---------------------------------------------------------
#  
# test
#
test: build_ext
	python `which nosetests` -v -x tests/

tox: tox26 tox27 tox33 tox34 tox35

tox26: swig build_ext26
	python2.6 `which tox` -e py26

tox27: swig build_ext27
	python2.7 `which tox` -e py27

tox33: swig build_ext33
	python3.3 `which tox` -e py33

tox34: swig build_ext34
	python3.4 `which tox` -e py34

tox35: swig build_ext35
	python3.5 `which tox` -e py35


# ---------------------------------------------------------
#  
# lint
# 
flakes: lint
lint: swig
	pyflakes tsip/*.py tests/*.py

# clean
#
clean: clean-build clean-pyc clean-test
	rm -fv ntpdshm/__init__.pyc
	rm -fv ntpdshm/shm.o
	rm -fv ntpdshm/shm.py
	rm -fv ntpdshm/shm.pyc
	rm -fv ntpdshm/_shm.so
	rm -fv ntpdshm/shm_wrap.c
	rm -fv ntpdshm/shm_wrap.o

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

