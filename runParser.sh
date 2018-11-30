#! /usr/bin/env sh

python parser.py ebay_data/items*.json

sqlite3 ebay.db < Schema/create.sql
sqlite3 ebay.db < Schema/load.txt
