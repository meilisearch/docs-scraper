# coding: utf-8
import pytest

from ...strategies.hierarchy import Hierarchy
from .abstract import get_strategy


@pytest.fixture
def get_hierarchy():
    hierarchy_variants = {
        'test_toplevel': {
            'lvl0': 'Foo',
            'lvl1': None,
            'lvl2': None,
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None
        },
        'test_sublevel': {
            'lvl0': 'Foo',
            'lvl1': 'Bar',
            'lvl2': 'Baz',
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None
        },
        'test_contentlevel': {
            'lvl0': 'Foo',
            'lvl1': 'Bar',
            'lvl2': 'Baz',
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None
        },
    }

    def _get_hierarchy(test_type):
        return hierarchy_variants.get(test_type)

    return _get_hierarchy


class TestGetHierarchyRadio:

    @pytest.mark.parametrize('level, test_type',
                             [
                                 ('lvl0', 'test_toplevel'),
                                 ('lvl2', 'test_sublevel'),
                                 ('content', 'test_contentlevel'),
                             ])
    def test_get_hierarchy_radio(self, get_hierarchy, level, test_type):
        # Given
        hierarchy = get_hierarchy(test_type)

        # When
        strategy = get_strategy()
        actual = Hierarchy.get_hierarchy_radio(hierarchy, level,
                                               strategy.levels)

        # Then
        if test_type == 'test_toplevel':
            assert actual['lvl0'] == 'Foo'
        else:
            assert actual['lvl0'] is None
        assert actual['lvl1'] is None
        if test_type == 'test_sublevel':
            assert actual['lvl2'] == 'Baz'
        else:
            assert actual['lvl2'] is None
        assert actual['lvl3'] is None
        assert actual['lvl4'] is None
        assert actual['lvl5'] is None
        assert actual['lvl6'] is None
