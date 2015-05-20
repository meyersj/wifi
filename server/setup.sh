#!/bin/bash
set -e

virtual=$PWD/env/bin
rm -rf env
virtualenv env
$virtual/pip install -r requirements.txt
cp -n sample-config.py config.py
