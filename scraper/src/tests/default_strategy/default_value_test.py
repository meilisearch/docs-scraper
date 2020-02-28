# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestGetRecordsFromDomWithDefaultValue:
    def test_default_value(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': 'h1',
                    'default_value': 'Documentation'
                },
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        # First record has the global H1
        assert len(actual) == 3
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] == 'Documentation'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'

    def test_default_value_for_text(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': 'h1',
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': {
                    'selector': 'p',
                    'default_value': 'Documentation'
                }
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>Foo</h1>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        # First record has the global H1
        assert len(actual) == 3
        assert actual[0]['type'] == 'lvl0'
        assert actual[0]['hierarchy']['lvl0'] == 'Foo'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'Documentation'

    def test_default_value_with_global(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': 'h1',
                    'global': True,
                    'default_value': 'Documentation'
                },
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })

        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        # First record has the global H1
        assert len(actual) == 3
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] == 'Documentation'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'

    def test_default_value_should_not_override(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': 'h1',
                    'global': True,
                    'default_value': 'Documentation'
                },
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>Foo</h1>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        # First record has the global H1
        assert len(actual) == 3
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] == 'Foo'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'

    def test_default_value_empty(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': 'h1',
                    'default_value': 'Documentation'
                },
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1></h1>
            <p>text</p>git
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        # First record has the global H1
        assert len(actual) == 4
        assert actual[0]['type'] == 'lvl0'
        assert actual[0]['hierarchy']['lvl0'] == 'Documentation'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] is None

    def test_default_value_empty_and_global(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': 'h1',
                    'global': 'true',
                    'default_value': 'Documentation'
                },
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
            <h1></h1>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()
        # Then

        # First record has the global H1
        assert len(actual) == 3
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] == 'Documentation'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'
