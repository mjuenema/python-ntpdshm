


all: clean build_ext


sdist: clean swig
	python setup.py sdist

bdist: clean swig
	python setup.py bdist

rpm: clean swig
	python setup.py bdist_rpm

build_ext: clean swig
	#python setup.py build_ext
	python setup.py build_ext --inplace

swig: clean
	( cd ntpdshm ; swig -python shm.i )

test: build_ext
	python `which nosetests` -v tests/

clean:
	rm -fv ntpdshm/__init__.pyc
	rm -fv ntpdshm/shm.o
	rm -fv ntpdshm/shm.py
	rm -fv ntpdshm/shm.pyc
	rm -fv ntpdshm/_shm.so
	rm -fv ntpdshm/shm_wrap.c
	rm -fv ntpdshm/shm_wrap.o
	rm -rfv build/

