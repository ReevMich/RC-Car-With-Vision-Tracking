#!/bin/bash

shopt -s extglob
rm -rfi !(__init__.py|init.sh|setup.py|test.py|DS4.c|DS4.i|DS4.h)
python setup.py build_ext --inplace

