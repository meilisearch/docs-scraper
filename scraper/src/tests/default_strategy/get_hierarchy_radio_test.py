# coding: utf-8
from .abstract import get_strategy
from ...strategies.hierarchy import Hierarchy


class TestGetHierarchyRadio:
    def test_toplevel(self):
        # Given
        hierarchy = {
            'lvl0': 'Foo',
            'lvl1': None,
            'lvl2': None,
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None
        }

        # When
        strategy = get_strategy()
        actual = Hierarchy.get_hierarchy_radio(hierarchy, 'lvl0',
                                               strategy.levels)

        # Then
        assert actual['lvl0'] == 'Foo'
        assert actual['lvl1'] is None
        assert actual['lvl2'] is None
        assert actual['lvl3'] is None
        assert actual['lvl4'] is None
        assert actual['lvl5'] is None
        assert actual['lvl6'] is None

    def test_sublevel(self):
        # Given
        hierarchy = {
            'lvl0': 'Foo',
            'lvl1': 'Bar',
            'lvl2': 'Baz',
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None
        }

        # When
        strategy = get_strategy()
        actual = Hierarchy.get_hierarchy_radio(hierarchy, 'lvl2',
                                               strategy.levels)

        # Then
        assert actual['lvl0'] is None
        assert actual['lvl1'] is None
        assert actual['lvl2'] == 'Baz'
        assert actual['lvl3'] is None
        assert actual['lvl4'] is None
        assert actual['lvl5'] is None
        assert actual['lvl6'] is None

    def test_contentlevel(self):
        # Given
        hierarchy = {
            'lvl0': 'Foo',
            'lvl1': 'Bar',
            'lvl2': 'Baz',
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None
        }

        # When
        strategy = get_strategy()
        actual = Hierarchy.get_hierarchy_radio(hierarchy, 'content',
                                               strategy.levels)

        # Then
        assert actual['lvl0'] is None
        assert actual['lvl1'] is None
        assert actual['lvl2'] is None
        assert actual['lvl3'] is None
        assert actual['lvl4'] is None
        assert actual['lvl5'] is None
        assert actual['lvl6'] is None
