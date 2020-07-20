FROM python:3.8.4-buster

WORKDIR /docs-scraper

COPY . .

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update -y \
    && apt-get install -y python3-pip
RUN pip3 install pipenv
RUN pipenv --python 3.8 install
