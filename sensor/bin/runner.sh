#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
PARENT=`dirname $SCRIPTPATH`

cd $PARENT

export PATH=$PATH:$SCRIPTPATH

./env/bin/python src/runner.py
