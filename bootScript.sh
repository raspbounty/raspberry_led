#!/bin/sh
cd ~/Documents/Raspberry/github/
/usr/bin/git pull
cd ledControl
python weatherLED.py
