# coding: utf-8
import pytest

from ...config.config_loader import ConfigLoader
from .abstract import config


class TestStopUrls:
    def test_stop_urls_accept_single_value(self):
        """ Allow passing stop_urls as string instead of array """
        # Given
        c = config({
            'stop_urls': ['www.foo.bar']
        })

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.stop_urls == ['www.foo.bar']

    def test_stop_urls_is_not_mandatory(self):
        """ Allow not passing stop_urls """
        # Given
        conf = config({
            'start_urls': ['http://www.starturl.com/']
        })

        with pytest.raises(Exception) as excinfo:
            # When
            ConfigLoader(conf)
            # Then
            assert 'start_urls should be list' in str(excinfo.value)
