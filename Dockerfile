FROM python:3-slim

LABEL description="Scanning APK file for URIs, endpoints & secrets."
LABEL repository="https://github.com/dwisiswant0/apkleaks"
LABEL maintainer="dwisiswant0"

WORKDIR /app

COPY requirements.txt .
RUN python -m ensurepip
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python", "/app/apkleaks.py"]
