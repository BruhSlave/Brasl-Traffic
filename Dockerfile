FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1
ENV SCREEN_SIZE=1800x1000x24

# Обновления и зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11vnc fluxbox curl git python3-pip procps  \
    libx11-6 libxext6 libxrender1 libxrandr2 libxv1 libxss1 libgl1-mesa-glx \
    && pip install --no-cache-dir pygame \
    && git clone --depth 1 https://github.com/novnc/noVNC.git /opt/novnc \
    && git clone --depth 1 https://github.com/novnc/websockify /opt/novnc/utils/websockify \
    && apt-get purge -y git curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /root/.cache

# Копирование приложения
COPY . /app
WORKDIR /app

EXPOSE 6080

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]

