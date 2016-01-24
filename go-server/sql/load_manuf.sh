#!/bin/bash

db=wifi
python manuf/download.py
psql -c "\copy data.manuf FROM manuf/manuf.csv csv" -d wifi
