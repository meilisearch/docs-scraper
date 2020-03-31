## Getting started

### Setting up the Python environment

[pipenv][1] is used to manage the whole Python environment.

- [Install pipenv][2] (this must be done only once)
- Run `pipenv install --dev` to create a Python virtual environment if
  unexisting and to install the Scraper's dependencies (this will have
  to be done each time dependencies are modified)
- Run `pipenv shell` to enter the Python virtual environment (this will have
  to be done each time you get back to work on the Scraper)

### Authentication

_WARNING:_ Please be aware that the scraper sends authentication headers to every scraped site, so use `allowed_domains` to adjust the scope accordingly!

#### Basic HTTP:

Basic HTTP authentication is supported by setting these environment variables:
- `DOCS_SCRAPER_BASICAUTH_USERNAME`
- `DOCS_SCRAPER_BASICAUTH_PASSWORD`

#### Cloudflare Access: Identity and Access Management

If it happens to you to scrape sites protected by Cloudflare Access, you
have to set appropriate HTTP headers. Values for these headers are taken
from env variables `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`.

In case of Google Cloud Identity-Aware Proxy, please specify these env variables:
- `IAP_AUTH_CLIENT_ID` - # pick [client ID of the application](https://console.cloud.google.com/apis/credentials) you are connecting to
- `IAP_AUTH_SERVICE_ACCOUNT_JSON` - # generate in [Actions](https://console.cloud.google.com/iam-admin/serviceaccounts) -> Create key -> JSON

### Installing Chrome Headless

Websites that need JavaScript for rendering are passed through ChromeDriver.
[Download the version][3] suited to your OS and then update the
`CHROMEDRIVER_PATH` in your `.env` file.

You should be ready to go.

### Running

See the dedicated page on [Algolia's documentation web site](https://community.algolia.com/docsearch/run-your-own.html).

## Lint code

The code is checked against linting rules by the CI, with `pylint`
(which is installed by `pipenv` as a dev package).

To run the linter, run the following command at the root of
your clone:
```bash
pipenv run pylint scraper cli deployer
```

## Run the tests

To run the full test suite, run `./docsearch test`.

## Reason of a fail from the docker image

To spot why a crawl fail without watching the logs, we have defined some custom
exit status:

| Exit code | Reason                                         |
|:---------:|------------------------------------------------|
|     3     | No record extracted from the crawl             |
|     4     | Too much hits returned from the crawl          |
|     5     | The configuration provided is not a valid JSON |
|     6     | The endpoint to call is incorrect              |
|     7     | Credentials used to request are not set        |


[1]: https://github.com/pypa/pipenv
[2]: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv
[3]: http://chromedriver.chromium.org/downloads
