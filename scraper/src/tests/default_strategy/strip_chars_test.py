# coding: utf-8
import lxml.html
import pytest

from .abstract import get_strategy


class TestGetRecordsFromDomWithStripChars:

    @pytest.mark.parametrize('selectors_lvl1, actual_lvl1',
                             [
                                 ('h2', '!Bar'),
                                 ({'selector': 'h2', 'strip_chars': '!'}, 'Bar.'),
                             ])
    def test_strip_chars(self, selectors_lvl1, actual_lvl1):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': 'h1',
                'lvl1': selectors_lvl1,
                'lvl2': 'h3',
                'content': 'p'
            },
            'strip_chars': ',.'
        })
        strategy.dom = lxml.html.fromstring('''
        <html><body>
            <h1>.Foo;</h1>
            <h2>!Bar.</h2>
            <h3>,Baz!</h3>
            <p>,text,</p>
        </body></html>
        ''')

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert len(actual) == 4
        assert actual[3]['type'] == 'content'
        assert actual[3]['hierarchy']['lvl0'] == 'Foo;'
        assert actual[3]['hierarchy']['lvl1'] == actual_lvl1
        assert actual[3]['hierarchy']['lvl2'] == 'Baz!'
        assert actual[3]['content'] == 'text'
