FROM algolia/docsearch-scraper-base
MAINTAINER Algolia <documentationsearch@algolia.com>

WORKDIR /root

# Copy DocSearch files
COPY . .
run touch .env
ENTRYPOINT ["pipenv", "run", "./docsearch", "test", "no_browser"]
