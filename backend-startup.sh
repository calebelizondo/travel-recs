#!/bin/bash

python3 -m venv venv
source ./venv/Scripts/activate
pip install -r ./requirements.txt
cd ./backend
python3 manage.py runserver