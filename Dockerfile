FROM python:3.8-slim-buster as build

LABEL description="Scanning APK file for URIs, endpoints & secrets."
LABEL repository="https://github.com/dwisiswant0/apkleaks"
LABEL maintainer="dwisiswant0"

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

FROM openjdk:slim-buster

COPY --from=build / /
ENTRYPOINT ["/app/apkleaks.py"]
