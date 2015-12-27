#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

rm -fr $SCRIPTPATH/env
virtualenv $SCRIPTPATH/env
cp -n $SCRIPTPATH/conf/sample-config.py $SCRIPTPATH/conf/config.py
$SCRIPTPATH/env/bin/pip install -r $SCRIPTPATH/conf/requirements.txt
