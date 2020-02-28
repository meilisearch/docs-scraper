# coding: utf-8
import pytest

from ...config.config_loader import ConfigLoader
from .abstract import config


class TestStartUrls:
    def test_mandatory_start_urls(self):
        """ Should throw if no start_urls passed """
        # Given
        c = config({
            'start_urls': None
        })

        # When / Then
        with pytest.raises(ValueError):
            ConfigLoader(c)

    def test_start_urls_doesnt_accept_single_value(self):
        """ Allow passing start_urls as string instead of array """
        # Given
        c = config({
            'start_urls': 'www.foo.bar'
        })

        with pytest.raises(Exception) as excinfo:
            # When
            ConfigLoader(c)
            # Then
            assert 'start_urls should be list' in str(excinfo.value)

    def test_start_urls_should_have_at_least_one_element(self):
        """ Should throw if start_urls does not have at least one element """
        # Given
        c = config({
            'start_urls': []
        })

        # When / Then
        with pytest.raises(ValueError):
            ConfigLoader(c)

    def test_start_url_should_add_default_page_rank_and_tags(self):
        """ Should add default values for page_rank and tags """
        # Given
        c = config({
            'start_urls': [{"url": "http://www.foo.bar/"}]
        })

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.start_urls[0]['tags'] == []
        assert actual.start_urls[0]['page_rank'] == 0

    def test_start_url_should_be_transform_to_object_if_string(self):
        """ Should accept strings for start_urls as well as objects """
        # Given
        c = config({
            'start_urls': ['http://www.foo.bar/']
        })

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.start_urls[0]['url'] == 'http://www.foo.bar/'

    def test_start_urls_should_be_generated_when_there_is_automatic_tagging_browser(
            self, monkeypatch):
        from .mocked_init import MockedInit
        monkeypatch.setattr("selenium.webdriver.chrome",
                            lambda x: MockedInit())
        monkeypatch.setattr("time.sleep", lambda x: "")

        # When
        c = config({
            "start_urls": [
                {
                    "url": "https://test.com/doc/(?P<version>.*?)/(?P<type_of_content>.*?)/",
                    "variables": {
                        "version": ["1.0", "1.1"],
                        "type_of_content": ["book", "bundles", "reference",
                                            "components", "cookbook",
                                            "best_practices"]
                    }
                }
            ]
        })

        actual = ConfigLoader(c)

        assert len(actual.start_urls) == 12
        assert actual.start_urls[0]['url'] == "https://test.com/doc/1.0/book/"
