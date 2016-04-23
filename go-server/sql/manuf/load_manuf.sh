#!/bin/bash

db=jeff
python download.py
#psql -c "\copy data.manuf FROM manuf.csv csv" -d ${db}
