# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestGetRecordsFromDomWithGlobalLevels:
    def test_global_title_at_the_end(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': 'h1',
                    'global': 'true'
                },
                'lvl1': 'h2',
                'lvl2': 'h3',
                'text': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
            <h1>Foo</h1>
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

        assert actual[2]['type'] == 'lvl2'
        assert actual[2]['hierarchy']['lvl0'] == 'Foo'
        assert actual[2]['hierarchy']['lvl1'] == 'Bar'
        assert actual[2]['hierarchy']['lvl2'] == 'Baz'

    def test_several_match_for_global_selector(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': 'h1',
                    'global': 'true'
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
            <h1>Foo</h1>
            <h1>Foo</h1>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert actual[2]['type'] == 'lvl2'
        assert actual[2]['hierarchy']['lvl0'] == 'Foo Foo'
        assert actual[2]['hierarchy']['lvl1'] == 'Bar'
        assert actual[2]['hierarchy']['lvl2'] == 'Baz'

    def test_several_global_selectors(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': 'h1',
                    'global': True
                },
                'lvl1': {
                    'selector': 'h2',
                    'global': 'true'
                },
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
            <h1>Foo</h1>
            <h1>Foo</h1>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] == 'Foo Foo'
        assert actual[0]['hierarchy']['lvl1'] == 'Bar'
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'

    def test_extra_global_attributes(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'lvl1': "h2",
                'lvl2': 'h3',
                'content': 'p',
                'extra_attr': '.test'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
            <h1>Foo</h1>
            <h1>Foo</h1>
            <span class="test">ok</span>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] is None
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'
        assert actual[0]['extra_attr'] == 'ok'

    def test_extra_global_attributes_with_xpath(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'lvl1': "h2",
                'lvl2': 'h3',
                'content': 'p',
                'extra_attr': {
                    "selector": "//*[@class='test']",
                    "type": "xpath"
                }
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
            <h1>Foo</h1>
            <h1>Foo</h1>
            <span class="test">ok</span>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] is None
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'
        assert actual[0]['extra_attr'] == 'ok'

    def test_extra_global_attributes_with_xpath_with_count(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'lvl1': "h2",
                'lvl2': 'h3',
                'content': 'p',
                'extra_attr': {
                    "selector": "count(//*[@class='test'])",
                    "type": "xpath"
                }
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
            <h1>Foo</h1>
            <h1>Foo</h1>
            <span class="test">ok</span>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] is None
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'
        assert actual[0]['extra_attr'] == 1
