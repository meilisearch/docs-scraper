# coding: utf-8
import lxml.html
import pytest

from ...strategies.anchor import Anchor
from .abstract import get_strategy


@pytest.fixture
def get_strategy_dom():
    strategy_dom_variants = {
        'test_name_on_heading': """
        <html><body>
            <h1>Foo</h1>
            <h2 name="bar">Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """,
        'test_id_not_in_a_direct_parent': """
        <div>
            <a id="bar"></a>
            <div>
                <div>
                    <h2>Bar</h2>
                </div>
            </div>
        </div>
        """,
        'test_id_on_heading': """
        <html><body>
            <h1>Foo</h1>
            <h2 id="bar">Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """,
        'test_anchor_in_subelement': """
        <html><body>
            <h1>Foo</h1>
            <h2><a href="#" name="bar">Bar</a><span></span></h2>
            <h3>Baz</h3>
        </body></html>
        """,
        "test_no_anchor": """
        <html><body>
            <h1>Foo</h1>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """,
    }

    def _get_strategy_dom(test_type):
        return strategy_dom_variants.get(test_type)

    return _get_strategy_dom


class TestGetAnchor:

    @pytest.mark.parametrize('level, anchor, test_type',
                             [
                                 ('lvl1', 'bar', 'test_name_on_heading'),
                                 ('lvl1', 'bar', 'test_id_not_in_a_direct_parent'),
                                 ('lvl1', 'bar', 'test_id_on_heading'),
                                 ('lvl1', 'bar', 'test_anchor_in_subelement'),
                                 ('lvl2', None, 'test_no_anchor'),
                             ])
    def test_get_anchor(self, get_strategy_dom, level, anchor, test_type):
        # Given
        strategy = get_strategy()
        strategy.dom = lxml.html.fromstring(get_strategy_dom(test_type))
        element = strategy.select(
            strategy.config.selectors['default'][level]['selector'])[0]

        # When
        actual = Anchor.get_anchor(element)

        # Then
        assert actual == anchor
