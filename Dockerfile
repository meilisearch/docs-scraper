FROM ubuntu:18.04

WORKDIR /docs-scraper

COPY . .

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update -y \
    && apt-get install -y python3-pip
RUN pip3 install pipenv
RUN pipenv install --python 3.6
