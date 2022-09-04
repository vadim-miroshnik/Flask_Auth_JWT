#!/bin/sh
flask deploy
echo Started
python3 pywsgi.py