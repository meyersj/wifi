#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 2
fi

if iwconfig | grep "mon0.*Mode:Monitor"; then
    # wifi monitor interface is running on mon0 so stop it
    airmon-ng stop mon0
fi
