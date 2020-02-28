#!/bin/sh
tag=$(git describe --abbrev=0 --tags)
read -r -p "Do you wish to also deploy $tag?" yn
case $yn in
    [Yy]* ) ./docsearch docker:build local_tag && docker push algolia/docsearch-scraper-base:"$tag" && docker push docsearch-scraper:"$tag";;
    [Nn]* ) ./docsearch docker:build;;
    * ) echo "Please answer yes or no, aborting."; exit 1;;
esac

docker push algolia/docsearch-scraper-base
docker push algolia/docsearch-scraper