# coding: utf-8
import pytest

from scraper.src.config.config_loader import ConfigLoader

from .abstract import config
from .mocked_init import MockedInit


class TestGetExtraFacets:
    def test_extra_facets_should_be_empty_by_default(self):
        c = config()

        actual = ConfigLoader(c)

        assert actual.get_extra_facets() == []

    @pytest.mark.chromedriver
    def test_extra_facets_should_be_set_from_start_urls_variables_browser(self,
                                                                          monkeypatch):
        monkeypatch.setattr("selenium.webdriver.chrome",
                            lambda x: MockedInit())

        c = config({
            "start_urls": [
                {
                    "url": "https://test.com/doc/(?P<type_of_content>.*?)/",
                    "variables": {
                        "type_of_content": ["book", "bundles", "reference",
                                            "components", "cookbook",
                                            "best_practices"]
                    }
                }
            ]
        })

        actual = ConfigLoader(c)

        assert actual.get_extra_facets() == ["type_of_content"]

    @pytest.mark.chromedriver
    def test_extra_facets_should_be_set_from_start_urls_variables_with_two_start_url_browser(
            self, monkeypatch):
        monkeypatch.setattr("selenium.webdriver.chrome",
                            lambda x: MockedInit())

        c = config({
            "js-render": True,
            "start_urls": [
                {
                    "url": "https://test.com/doc/(?P<type_of_content>.*?)/",
                    "variables": {
                        "type_of_content": ["book", "bundles", "reference",
                                            "components", "cookbook",
                                            "best_practices"]
                    }
                },
                {
                    "url": "https://test.com/doc/(?P<type_of_content>.*?)/",
                    "variables": {
                        "type_of_content": ["test"]
                    }
                }
            ]
        })

        actual = ConfigLoader(c)

        assert actual.get_extra_facets() == ["type_of_content"]

    @pytest.mark.chromedriver
    def test_extra_facets_should_be_set_from_start_urls_variables_with_multiple_tags_browser(
            self, monkeypatch):
        monkeypatch.setattr("selenium.webdriver.chrome",
                            lambda x: MockedInit())

        c = config({
            "start_urls": [
                {
                    "url": "https://test.com/doc/(?P<type_of_content>.*?)/(?P<version>.*?)",
                    "variables": {
                        "type_of_content": ["book", "bundles", "reference",
                                            "components", "cookbook",
                                            "best_practices"],
                        "version": ["1.0", "2.0"]
                    }
                },
                {
                    "url": "https://test.com/doc/(?P<type_of_content>.*?)/",
                    "variables": {
                        "type_of_content": ["test"]
                    }
                }
            ]
        })

        actual = ConfigLoader(c)

        extra_facets = actual.get_extra_facets()

        assert "version" in extra_facets
        assert "type_of_content" in extra_facets
