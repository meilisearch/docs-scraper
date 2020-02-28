# coding: utf-8
from ...config.config_loader import ConfigLoader
from .abstract import config
import pytest


class TestSitemap:
    def test_need_sitemap_urls_force_sitemap(self):
        """ Should throw if CONFIG need sitemap_urls """
        # Given

        urls_sitemap_less = config({'force_sitemap_urls_crawling': True})

        # When / Then
        with pytest.raises(Exception):
            ConfigLoader(urls_sitemap_less)

    def test_need_sitemap_urls_regex(self):
        """ Should throw if CONFIG need sitemap_urls """
        urls_sitemap_less = {
            'sitemap_urls_regexs': ["/doc/"]

        }

        # When / Then
        with pytest.raises(Exception):
            ConfigLoader(urls_sitemap_less)

    def test_config_loader(self):
        """ Should throw if CONFIG need sitemap_urls """
        additional_config = {
            'sitemap_urls_regexs': ["/doc/", "/docs/"],
            'force_sitemap_urls_crawling': True,
            'sitemap_urls': ["http://www.test.com/sitemap.xml",
                             "http://www.test.com/doc/sitemap.xml"]

        }

        config_loaded = ConfigLoader(config(additional_config))
        # When / Then
        assert "http://www.test.com/sitemap.xml" in config_loaded.sitemap_urls
        assert "http://www.test.com/doc/sitemap.xml" in config_loaded.sitemap_urls
        assert "/doc/" in config_loaded.sitemap_urls_regexs
        assert config_loaded.force_sitemap_urls_crawling
