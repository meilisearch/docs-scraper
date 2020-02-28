# coding: utf-8
from ...config.config_loader import ConfigLoader
from .abstract import config


class TestDomains:
    def test_allowed_domains_start(self):
        """ Should populate allowed_domains from start_urls """
        # Given
        c = config({
            'start_urls': ['http://www.foo.bar/'],
            'stop_urls': [],
            'allowed_domains': None
        })

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.allowed_domains == ['www.foo.bar']

    def test_allowed_domains_start_stop(self):
        """ Should populate allowed_domains from both start and stop urls """
        # Given
        c = config({
            'start_urls': ['http://www.foo.bar/'],
            'stop_urls': ['http://www.algolia.com/'],
            'allowed_domains': None
        })

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.allowed_domains == ['www.foo.bar', 'www.algolia.com']

    def test_allowed_domains_unique(self):
        """ Should populate a list of unique domains """
        # Given
        c = config({
            'start_urls': ['http://www.foo.bar/'],
            'stop_urls': [
                'http://www.algolia.com/',
                'http://www.foo.bar/'
            ],
            'allowed_domains': None
        })

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.allowed_domains == ['www.foo.bar', 'www.algolia.com']

    def test_not_allowed_domains_accept_single_value(self):
        """ Should allow passing allowed_domains as a string instead of an array
        """
        # Given
        c = config({
            'allowed_domains': ['www.foo.bar']
        })

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.allowed_domains == ['www.foo.bar']
