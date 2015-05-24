#!/bin/bash

virtual=$PWD/env/bin
archive=KimiNewt-pyshark-v0.3.4-20-geb4f2b9.tar.gz
install=KimiNewt-pyshark-eb4f2b9/src

rm -fr env
virtualenv env
cp -n sample-config.py config.py
$virtual/pip install -r requirements.txt
cd lib
tar xzvf ${archive}
cd ${install}
$virtual/python setup.py install
