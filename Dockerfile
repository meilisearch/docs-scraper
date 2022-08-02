FROM python:3.8.4-buster

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /docs-scraper

RUN apt-get update -y \
    && apt-get install -y python3-pip libnss3 \
    && apt-get install -y chromium-driver

RUN pip3 install pipenv


COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock 

RUN pipenv --python 3.8 install


COPY . . 
