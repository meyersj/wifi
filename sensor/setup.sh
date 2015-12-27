#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

rm -fr $SCRIPTPATH/env
virtualenv $SCRIPTPATH/env
cp -n $SCRIPTPATH/sample-config.py $SCRIPTPATH/config.py
$SCRIPTPATH/env/bin/pip install -r $SCRIPTPATH/requirements.txt
