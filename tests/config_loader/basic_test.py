# coding: utf-8
import re
from scraper.src.config.version import __version__, qualified_version
from scraper.src.config.config_loader import ConfigLoader
from .abstract import config
import pytest


class TestInit:
    @staticmethod
    def test_need_json_env_var():
        """ Should throw if CONFIG is not JSON """
        # Given
        c = 'foobar'

        # When / Then
        with pytest.raises(ValueError):
            ConfigLoader(c)

    def test_mandatory_index_uid(self):
        """ Should throw if no index_uid passed """
        # Given
        c = config({
            'index_uid': None
        })

        # When / Then
        with pytest.raises(ValueError):
            ConfigLoader(c)

    def test_correct_new_naming_scrape(self):
        """ Old variable scrap_url must be spread to scrape_url. If one is defined, the previous one must be used"""
        # Given
        c = config({
            'scrap_start_urls': False
        })

        config_loaded = ConfigLoader(c)

        assert config_loaded.scrape_start_urls == False
        assert config_loaded.scrap_start_urls == config_loaded.scrape_start_urls

    def test_excpetion_when_shadowing_(self):
        """ User must use the last attribute name: scrape_start_urls, not both (BC). This error must be raised"""
        # Given
        c = config({
            'scrap_start_urls': False,
            'scrape_start_urls': False
        })

        with pytest.raises(Exception):
            ConfigLoader(c)

    def test_get_qualified_version(self):
        """ Old variable scrap_url must be spread to scrape_url. If one is defined, the previous one must be used"""
        c = config({
            'user_agent': qualified_version()
        })

        config_loaded = ConfigLoader(c)

        assert config_loaded.user_agent == f"Meilisearch DocsScraper (v{__version__})"
