#!/bin/bash
set -e

db=wifi

python download_oui.py
psql -c "DROP DATABASE IF EXISTS ${db}" -d postgres
psql -c "CREATE DATABASE ${db}" -d postgres
psql -f create.sql -d ${db}
psql -c "\copy data.manuf FROM oui_lookup.csv csv" -d ${db}
rm oui_lookup.csv
