#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

$SCRIPTPATH/env/bin/newrelic-admin run-program $SCRIPTPATH/runner.py
