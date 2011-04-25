#!/bin/bash

echo "Downloading..."
VID_PATH=$(python youtube-dl.py $1 | awk '/Destination/ {print $3}')

echo "Dumping audio..."
mplayer -vc dummy -vo null -ao pcm $VID_PATH > /dev/null 2>&1

echo "Analyzing..."
ENDPOINTS=$(python clip.py audiodump.wav)
echo "$ENDPOINTS seconds (start, end)"

