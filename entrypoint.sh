#!/bin/bash
set -e

# Запуск виртуального X-сервера
Xvfb :1 -screen 0 ${SCREEN_SIZE} &
sleep 2

# Старт оконного менеджера
fluxbox &
sleep 1

# Старт x11vnc
x11vnc -display :1 -noxdamage -forever -shared -nopw -bg -rfbport 5900
sleep 1

# Старт веб-прокси
/opt/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &
sleep 1

# Запуск pygame-приложения
python3 main.py
