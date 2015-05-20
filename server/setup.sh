#!/bin/bash
set -e

virtual=$PWD/env/bin
rm -rf env
virtaulenv env
$virtual/pip install -r requirments.txt
cp -n sample-config.py config.py
