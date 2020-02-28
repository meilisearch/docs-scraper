FROM algolia/docsearch-scraper-base
MAINTAINER Algolia <documentationsearch@algolia.com>

WORKDIR /root
COPY scraper/src ./src

ENTRYPOINT ["pipenv", "run", "python", "-m", "src.index"]
