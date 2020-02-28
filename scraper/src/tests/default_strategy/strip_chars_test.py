# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestGetRecordsFromDomWithStripChars:
    def test_strip_chars(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                "lvl0": "h1",
                "lvl1": "h2",
                "lvl2": "h3",
                "content": "p"
            },
            'strip_chars': ',.'
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>.Foo;</h1>
            <h2>!Bar.</h2>
            <h3>,Baz!</h3>
            <p>,text,</p>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert len(actual) == 4
        assert actual[3]['type'] == 'content'
        assert actual[3]['hierarchy']['lvl0'] == 'Foo;'
        assert actual[3]['hierarchy']['lvl1'] == '!Bar'
        assert actual[3]['hierarchy']['lvl2'] == 'Baz!'
        assert actual[3]['content'] == 'text'

    def test_strip_chars_with_level_override(self):
        # Given
        strategy = get_strategy({
            'strip_chars': ',.',
            'selectors': {
                "lvl0": "h1",
                "lvl1": {
                    "selector": "h2",
                    "strip_chars": "!"
                },
                "lvl2": "h3",
                "content": "p"
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>.Foo;</h1>
            <h2>!Bar.</h2>
            <h3>,Baz!</h3>
            <p>,text,</p>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert len(actual) == 4
        assert actual[3]['type'] == 'content'
        assert actual[3]['hierarchy']['lvl0'] == 'Foo;'
        assert actual[3]['hierarchy']['lvl1'] == 'Bar.'
        assert actual[3]['hierarchy']['lvl2'] == 'Baz!'
        assert actual[3]['content'] == 'text'
