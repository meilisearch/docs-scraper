FROM python:3.10.8-slim-bullseye

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /docs-scraper

RUN apt-get update -y && apt-get install -y python3-pip libnss3 chromium-driver

RUN pip3 install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install

COPY . .
