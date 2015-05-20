#!/bin/bash

virtual=$PWD/env/bin

rm -fr env
virtualenv env
cp -n sample-config.py config.py
$virtual/pip install -r requirements.txt
cd lib/KimiNewt-pyshark-03c4d4c/src
$virtual/python setup.py install
