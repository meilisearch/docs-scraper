# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestGetRecordsFromDomWithMinIndexedLevel:
    def test_test_default_value_with_global(self):
        """ Should be able to not index the n first levels """
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': 'h1',
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p',
            },
            'min_indexed_level': 2
        })

        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1>Foo</h1>
            <h2>Bar</h2>
            <h3>Baz</h3>
            <p>text</p>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert len(actual) == 2
        assert actual[0]['type'] == 'lvl2'
        assert actual[0]['hierarchy']['lvl0'] == 'Foo'
        assert actual[0]['hierarchy']['lvl1'] == 'Bar'
        assert actual[0]['hierarchy']['lvl2'] == 'Baz'
        assert actual[1]['type'] == 'content'
