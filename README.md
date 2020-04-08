# Docs Scraper <!-- omit in TOC -->

A scraper for your documentation website that indexes the scraped content into a MeiliSearch instance.

- [Installation and Usage](#installation-and-usage)
  - [From Source Code](#from-source-code)
  - [With Docker](#with-docker)
  - [In a GitHub Action](#in-a-github-action)
  - [About the API Key](#about-the-api-key)
- [Configuration file](#configuration-file)
- [And for the search bar?](#and-for-the-search-bar)
- [Development Workflow](#development-workflow)
- [Credits](#credits)


## Installation and Usage

This project supports Python 3.6+.

### From Source Code

Set both environment variables `MEILISEARCH_HOST_URL` and `MEILISEARCH_API_KEY`.

Then, run:
```bash
$ pipenv install
$ pipenv run ./docs_scraper run <path-to-your-config-file>
```

### With Docker

```bash
$ docker run -t --rm \
    -e MEILISEARCH_HOST_URL=<your-meilisearch-host-url> \
    -e MEILISEARCH_API_KEY=<your-meilisearch-api-key> \
    -v <absolute-path-to-your-config-file>:/docs-scraper/config.json \
    getmeili/docs-scraper:v0.9.0 pipenv run ./docs_scraper config.json
```

### In a GitHub Action

To run after your deployment job:

```yml
run-scraper:
    needs: <your-deployment-job>
    runs-on: ubuntu-18.04
    steps:
    - uses: actions/checkout@master
    - name: Run scraper
      env:
        HOST_URL: ${{ secrets.MEILISEARCH_HOST_URL }}
        API_KEY: ${{ secrets.MEILISEARCH_API_KEY }}
        CONFIG_FILE_PATH: <path-to-your-config-file>
      run: |
        docker run -t --rm \
          -e MEILISEARCH_HOST_URL=$HOST_URL \
          -e MEILISEARCH_API_KEY=$API_KEY \
          -v $CONFIG_FILE_PATH:/docs-scraper/config.json \
          getmeili/docs-scraper:v0.9.0 pipenv run ./docs_scraper config.json
```

Here is the [GitHub Action file](https://github.com/meilisearch/documentation/blob/master/.github/workflows/gh-pages-scraping.yml) we use in production for the MeiliSearch documentation.

### About the API Key

The API key you must provide as environment variable should have the permissions to add documents into your MeiliSearch instance.

Thus, you need to provide the private key or the master key.

_More about [MeiliSearch authentication](https://docs.meilisearch.com/guides/advanced_guides/authentication.html)._

## Configuration file

A generic configuration file:

```json
{
  "index_uid": "docs",
  "start_urls": ["https://www.example.com/doc/"],
  "sitemap_urls": ["https://www.example.com/sitemap.xml"],
  "stop_urls": [],
  "selectors": {
    "lvl0": {
      "selector": ".docs-lvl0",
      "global": true,
      "default_value": "Documentation"
    },
    "lvl1": {
      "selector": ".docs-lvl1",
      "global": true,
      "default_value": "Chapter"
    },
    "lvl2": ".docs-content .docs-lvl2",
    "lvl3": ".docs-content .docs-lvl3",
    "lvl4": ".docs-content .docs-lvl4",
    "lvl5": ".docs-content .docs-lvl5",
    "lvl6": ".docs-content .docs-lvl6",
    "text": ".docs-content p, .docs-content li"
  }
}
```

The scraper will focus on the highlighted information depending on your selectors.

Here is the [configuration file](https://github.com/meilisearch/documentation/blob/master/.vuepress/scraper/config.json) we use for the MeiliSearch documentation.

## And for the search bar?

After having crawled your documentation, you might need a search bar to improve your user experience!

For the front part, check out the [docs-searchbar.js repository](https://github.com/meilisearch/docs-searchbar.js), wich provides a front-end search bar adapted for documentation.

## Development Workflow

### Install and Launch <!-- omit in TOC -->

Set both environment variables `MEILISEARCH_HOST_URL` and `MEILISEARCH_API_KEY`.

Then, run:
```bash
$ pipenv install
$ pipenv run ./docs_scraper run <path-to-your-config-file>
```

### Release <!-- omit in TOC -->

Once the changes are merged on `master`, in your terminal, you must be on the `master` branch and push a new tag with the right version:

```bash
$ git checkout master
$ git pull origin master
$ git tag vX.X.X
$ git push --tag origin master
```

A GitHub Action will be triggered and push the `latest` and `vX.X.X` version of Docker image on [DockerHub](https://hub.docker.com/repository/docker/getmeili/docs-scraper)

## Credits

Based on [Algolia's docsearch scraper repository](https://github.com/algolia/docsearch-scraper) from [this commit](https://github.com/curquiza/docsearch-scraper/commit/aab0888989b3f7a4f534979f0148f471b7c435ee).<br>
Due to a lot of future changes on this repository compared to the original one, we don't maintain it as an official fork.
