FROM python:3.10.8-slim-bullseye

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /docs-scraper

RUN : \
  && apt-get update -y \
  && apt-get install -y --no-install-recommends \
  libnss3 \
  chromium-driver \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && pip install pipenv --no-cache-dir

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install

COPY . .
