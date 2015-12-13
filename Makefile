


all: clean build_ext


build_ext: swig
	python setup.py build_ext

swig:
	( cd ntpdshm ; swig -python ntpdshm.i )



clean:
	rm -fv ntpdshm/__init__.pyc
	rm -fv ntpdshm/ntpdshm.o
	rm -fv ntpdshm/ntpdshm.py
	rm -fv ntpdshm/ntpdshm.pyc
	rm -fv ntpdshm/_ntpdshm.so
	rm -fv ntpdshm/ntpdshm_wrap.c
	rm -fv ntpdshm/ntpdshm_wrap.o

