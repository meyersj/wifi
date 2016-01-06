#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 2
fi

if iwconfig | grep -q "mon0.*Mode:Monitor" ; then
    echo "running"
else
    if airmon-ng start wlan0 | grep "monitor mode enabled on mon0" ; then
        echo "started"     
        exit 0
    else
        echo "not started"
        exit 1
    fi
fi
