#!/bin/bash
cd ./backend
pip install --upgrade pip
pip install -r ./requirements.txt
python3 manage.py runserver