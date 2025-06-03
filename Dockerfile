FROM python:3.11-slim

ENV DISPLAY=:1
ENV SCREEN_SIZE=1800x1000x24

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    xvfb x11vnc fluxbox \
    python3-pip git curl net-tools \
    && pip install pygame \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка noVNC и websockify
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc \
    && git clone https://github.com/novnc/websockify /opt/novnc/utils/websockify

# Копируем приложение
COPY . /app
WORKDIR /app

EXPOSE 6080  

# Скрипт запуска
CMD bash -c "\
    Xvfb :1 -screen 0 ${SCREEN_SIZE} & \
    fluxbox & \
    x11vnc -display :1 -nopw -forever -shared -bg -rfbport 5900 && \
    /opt/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 & \
    python3 main.py"
