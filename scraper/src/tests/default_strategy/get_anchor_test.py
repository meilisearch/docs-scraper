# coding: utf-8
import lxml.html
from .abstract import get_strategy
from ...strategies.anchor import Anchor


class TestGetAnchor:
    def test_name_on_heading(self):
        # Given
        strategy = get_strategy()
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>Foo</h1>
            <h2 name="bar">Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """)
        level = 'lvl1'
        element = strategy.select(
            strategy.config.selectors['default'][level]['selector'])[0]

        # When
        actual = Anchor.get_anchor(element)

        # Then
        assert actual == 'bar'

    def test_id_not_in_a_direct_parent(self):
        strategy = get_strategy()
        strategy.dom = lxml.html.fromstring("""
        <div>
            <a id="bar"></a>
            <div>
                <div>
                    <h2>Bar</h2>
                </div>
            </div>
        </div>
        """)

        level = 'lvl1'
        element = strategy.select(
            strategy.config.selectors['default'][level]['selector'])[0]

        # When
        actual = Anchor.get_anchor(element)

        # Then
        assert actual == 'bar'

    def test_id_on_heading(self):
        # Given
        strategy = get_strategy()
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>Foo</h1>
            <h2 id="bar">Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """)
        level = 'lvl1'
        element = strategy.select(
            strategy.config.selectors['default'][level]['selector'])[0]

        # When
        actual = Anchor.get_anchor(element)

        # Then
        assert actual == 'bar'

    def test_anchor_in_subelement(self):
        # Given
        strategy = get_strategy()
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>Foo</h1>
            <h2><a href="#" name="bar">Bar</a><span></span></h2>
            <h3>Baz</h3>
        </body></html>
        """)
        level = 'lvl1'
        element = strategy.select(
            strategy.config.selectors['default'][level]['selector'])[0]

        # When
        actual = Anchor.get_anchor(element)

        # Then
        assert actual == 'bar'

    def test_no_anchor(self):
        # Given
        strategy = get_strategy()
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>Foo</h1>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """)
        level = 'lvl2'
        element = strategy.select(
            strategy.config.selectors['default'][level]['selector'])[0]

        # When
        actual = Anchor.get_anchor(element)

        # Then
        assert actual is None
