#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
PARENT=`dirname $SCRIPTPATH`

cd $PARENT
./env/bin/python src/runner.py
