#!/bin/bash

virtual=$PWD/env/bin

rm -fr env
virtualenv env
cp -n sample-config.py config.py
$virtual/pip install -r requirements.txt
