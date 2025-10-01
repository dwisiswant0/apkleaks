FROM python:3-slim

LABEL description="Scanning APK file for URIs, endpoints & secrets."
LABEL repository="https://github.com/dwisiswant0/apkleaks"
LABEL maintainer="dwisiswant0"

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget unzip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Temurin JRE 17
RUN mkdir -p /opt/java && \
    wget -O /tmp/temurin.tar.gz https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jre_x64_linux_hotspot_17.0.9_9.tar.gz && \
    tar -xzf /tmp/temurin.tar.gz -C /opt/java --strip-components=1 && \
    rm /tmp/temurin.tar.gz

# Config JAVA_HOME and PATH
ENV JAVA_HOME=/opt/java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install jadx 1.2.0
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
