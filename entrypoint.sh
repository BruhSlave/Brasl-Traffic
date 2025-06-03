#!/bin/bash
set -e

export DISPLAY=:1

Xvfb :1 -screen 0 ${SCREEN_SIZE} &
sleep 2

fluxbox &
sleep 1

x11vnc -display :1 -noxdamage -forever -shared -nopw -bg -rfbport 5900
sleep 1

/opt/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &
sleep 1

export DISPLAY=${DISPLAY:-:1}

echo "DISPLAY=$DISPLAY"
ls -l /app
python3 main.py
echo "main.py exited with $?"

python3 main.py
