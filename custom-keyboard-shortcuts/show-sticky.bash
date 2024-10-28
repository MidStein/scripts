#!/usr/bin/env bash

# put terminal on left
sleep 0.5
ydotool key 125:1 105:1 105:0 125:0 

sleep 0.5
# open krunner
ydotool key 56:1 57:1 57:0 56:0

sleep 0.5
ydotool type 'window sticky.pdf'

sleep 0.5
# press enter
ydotool key 28:1 28:0

sleep 0.5
ydotool key 56:1 15:1 15:0 56:0
