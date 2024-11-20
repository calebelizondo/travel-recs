#!/bin/bash
pip install --upgrade pip
pip install -r ./requirements.txt
cd ./backend
python3 manage.py runserver