#!/bin/bash
set -e

virtual=$PWD/env/bin
rm -rf env
virtaulenv env
$virtual/pip install -r requirments.txt

