# Contributing <!-- omit in TOC -->

First of all, thank you for contributing to Meilisearch! The goal of this document is to provide everything you need to know in order to contribute to Meilisearch and its different integrations.

- [Assumptions](#assumptions)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Git Guidelines](#git-guidelines)
- [Release Process (for internal team only)](#release-process-for-internal-team-only)

## Assumptions

1. **You're familiar with [GitHub](https://github.com) and the [Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)(PR) workflow.**
2. **You've read the Meilisearch [documentation](https://www.meilisearch.com/docs) and the [README](/README.md).**
3. **You know about the [Meilisearch community](https://discord.com/invite/meilisearch). Please use this for help.**

## How to Contribute

1. Make sure that the contribution you want to make is explained or detailed in a GitHub issue! Find an [existing issue](https://github.com/meilisearch/docs-scraper/issues/) or [open a new one](https://github.com/meilisearch/docs-scraper/issues/new).
2. Once done, [fork the docs-scraper repository](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) in your own GitHub account. Ask a maintainer if you want your issue to be checked before making a PR.
3. [Create a new Git branch](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-and-deleting-branches-within-your-repository).
4. Review the [Development Workflow](#development-workflow) section that describes the steps to maintain the repository.
5. Make the changes on your branch.
6. [Submit the branch as a PR](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) pointing to the `main` branch of the main docs-scraper repository. A maintainer should comment and/or review your Pull Request within a few days. Although depending on the circumstances, it may take longer.<br>
 We do not enforce a naming convention for the PRs, but **please use something descriptive of your changes**, having in mind that the title of your PR will be automatically added to the next [release changelogs](https://github.com/meilisearch/docs-scraper/releases/).

## Development Workflow

### Install and Launch <!-- omit in TOC -->

The [`pipenv` command](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) must be installed.

Set both environment variables `MEILISEARCH_HOST_URL` and `MEILISEARCH_API_KEY`.

Then, run:

```bash
pipenv install
pipenv run ./docs_scraper <path-to-your-config-file>
```

### Linter and Tests <!-- omit in TOC -->

```bash
pipenv install --dev
# Linter
pipenv run pylint scraper
```

If you have [a `chromedriver`](https://sites.google.com/chromium.org/driver/), you can run the full test suite by passing the path to your `chromedriver`.

```bash
pipenv run pytest --chromedriver=/path/to/your/chromedriver
```

Where `path/to/your/chromedriver` matches your particular path. If you are unsure of your `chromedriver` path you find it on Linux/Mac with:


```bash
which chromedriver
```

Or on Windwos with:

```bash
where chromedriver
```

It is possible when running the tests that an error occurs if your running chrome browser has a different version than your chromedriver. In which case, please download the adequate [chromedriver](https://sites.google.com/chromium.org/driver/).

If you do not have `chromedriver` installed you can skip the tests that require it by running the tests with:

```bash
pipenv run pytest -m "not chromedriver"
```

Note that these tests will still run in CI when you submit your pull request.

Optionally tox can be used to run test on all supported version of Python and linting.

```bash
pipenv run tox -- --chromedriver=/path/to/your/chromedriver
```

Or to run tox if you don't have chromedriver

```bash
pipenv run tox -- -m "not chromedriver"
```

## Git Guidelines

### Git Branches <!-- omit in TOC -->

All changes must be made in a branch and submitted as PR.
We do not enforce any branch naming style, but please use something descriptive of your changes.

### Git Commits <!-- omit in TOC -->

As minimal requirements, your commit message should:
- be capitalized
- not finish by a dot or any other punctuation character (!,?)
- start with a verb so that we can read your commit message this way: "This commit will ...", where "..." is the commit message.
  e.g.: "Fix the home page button" or "Add more tests for create_index method"

We don't follow any other convention, but if you want to use one, we recommend [this one](https://chris.beams.io/posts/git-commit/).

### GitHub Pull Requests <!-- omit in TOC -->

Some notes on GitHub PRs:

- [Convert your PR as a draft](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/changing-the-stage-of-a-pull-request) if your changes are a work in progress: no one will review it until you pass your PR as ready for review.<br>
  The draft PR can be very useful if you want to show that you are working on something and make your work visible.
- The branch related to the PR must be **up-to-date with `main`** before merging. Fortunately, this project [integrates a bot](https://github.com/meilisearch/integration-guides/blob/main/resources/bors.md) to automatically enforce this requirement without the PR author having to do it manually.
- All PRs must be reviewed and approved by at least one maintainer.
- The PR title should be accurate and descriptive of the changes. The title of the PR will be indeed automatically added to the next [release changelogs](https://github.com/meilisearch/docs-scraper/releases/).

## Release Process (for the internal team only)

Meilisearch tools follow the [Semantic Versioning Convention](https://semver.org/).

### Automation to Rebase and Merge the PRs <!-- omit in TOC -->

This project integrates a bot that helps us manage pull requests merging.<br>
_[Read more about this](https://github.com/meilisearch/integration-guides/blob/main/resources/bors.md)._

### Automated Changelogs <!-- omit in TOC -->

This project integrates a tool to create automated changelogs.<br>
_[Read more about this](https://github.com/meilisearch/integration-guides/blob/main/resources/release-drafter.md)._

### How to Publish the Release <!-- omit in TOC -->

⚠️ Before doing anything, make sure you got through the guide about [Releasing an Integration](https://github.com/meilisearch/integration-guides/blob/main/resources/integration-release.md).

Make a PR modifying the file [`scraper/src/config/version.py`](/scraper/src/config/version.py) with the right version.

```python
__version__ = "X.X.X"
```

Once the changes are merged on `main`, you can publish the current draft release via the [GitHub interface](https://github.com/meilisearch/docs-scraper/releases): on this page, click on `Edit` (related to the draft release) > update the description (be sure you apply [these recommendations](https://github.com/meilisearch/integration-guides/blob/main/resources/integration-release.md#writting-the-release-description)) > when you are ready, click on `Publish release`.

GitHub Actions will be triggered and push the `latest` and `vX.X.X` version of the Docker image to [DockerHub](https://hub.docker.com/repository/docker/getmeili/docs-scraper).

<hr>

Thank you again for reading this through. We can not wait to begin to work with you if you make your way through this contributing guide ❤️
