# coding: utf-8
from .abstract import get_strategy
from ...strategies.algolia_settings import AlgoliaSettings


class TestGetSettings:
    def test_get_settings(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                "lvl0": "h1",
                "lvl1": "h2",
                "lvl2": "h3",
                "content": "p"
            }
        })

        # When
        settings = AlgoliaSettings.get(strategy.config, strategy.levels)

        # Then
        expected_settings = [
            'unordered(hierarchy_radio_camel.lvl0)',
            'unordered(hierarchy_radio.lvl0)',
            'unordered(hierarchy_radio_camel.lvl1)',
            'unordered(hierarchy_radio.lvl1)',
            'unordered(hierarchy_radio_camel.lvl2)',
            'unordered(hierarchy_radio.lvl2)',
            'unordered(hierarchy_camel.lvl0)',
            'unordered(hierarchy.lvl0)',
            'unordered(hierarchy_camel.lvl1)',
            'unordered(hierarchy.lvl1)',
            'unordered(hierarchy_camel.lvl2)',
            'unordered(hierarchy.lvl2)',
            'content'
        ]

        assert settings['attributesToIndex'] == expected_settings
