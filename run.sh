#!/bin/bash

python3 src/db_init.py 
python3 src/fill_tables.py 
python3 src/main.py
