# coding: utf-8
from ...config.config_loader import ConfigLoader
from .abstract import config


class TestSelectorsExclude:
    def test_selectors_exclude_default(self):
        """ Should set the `selectors_exclude` parameter to [] by default """

        c = config()

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.selectors_exclude == []

    def test_selectors_exclude_set_override_default(self):
        """ Default `selectors_exclude` should be override when set in the config """
        # When
        c = config({
            'selectors_exclude': ['.test']
        })

        # When
        actual = ConfigLoader(c)

        # Then
        assert actual.selectors_exclude == ['.test']

    def test_selectors_exclude_is_not_mandatory(self):
        """ Allow not passing selectors_exclude """
        # Given
        conf = config({
            'allowed_domains': 'allowed_domains',
            'api_key': 'api_key',
            'app_id': 'app_id',
            'index_name': 'index_name',
            'selectors': [],
            'start_urls': ['http://www.starturl.com/'],
            'stop_urls': ['http://www.stopurl.com/']
        })

        # When
        actual = ConfigLoader(conf)

        # Then
        assert actual.selectors_exclude == []
