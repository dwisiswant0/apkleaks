FROM python:3-slim

LABEL description="Scanning APK file for URIs, endpoints & secrets."
LABEL repository="https://github.com/dwisiswant0/apkleaks"
LABEL maintainer="dwisiswant0"

RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless && \
    apt-get install -y unzip && \
    rm -rf /var/lib/apt/lists/*

# Instal jadx 1.2.0
ADD https://github.com/skylot/jadx/releases/download/v1.2.0/jadx-1.2.0.zip /tmp/jadx.zip
RUN unzip /tmp/jadx.zip -d /opt/jadx && \
    rm /tmp/jadx.zip && \
    ln -s /opt/jadx/bin/jadx /usr/local/bin/jadx

WORKDIR /app

COPY requirements.txt .
RUN python -m ensurepip
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python", "/app/apkleaks.py"]
