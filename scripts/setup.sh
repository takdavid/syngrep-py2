#!/usr/bin/env bash
set -x
set -e
[ -d venv ] || virtualenv --python=python2.7 venv
[ -f a ] || ln -s venv/bin/activate a
. a
python setup.py install
