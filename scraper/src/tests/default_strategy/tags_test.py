# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestTags:
    def test_adding_tags_for_page(self):
        # Given
        strategy = get_strategy({
            'start_urls': [{
                'url': 'http://foo.bar/api',
                'tags': ["test"]
            }],
            'selectors': {
                "lvl0": "h1",
                "lvl1": "h2",
                "lvl2": "h3",
                "content": "p"
            }
        })

        strategy.dom = lxml.html.fromstring("""
        <html><body>
         <h1>Foo</h1>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom("http://foo.bar/api")

        # Then
        assert actual[0]['tags'] == ["test"]

    def test_adding_tags_for_subpage(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                "lvl0": "h1",
                "lvl1": "h2",
                "lvl2": "h3",
                "content": "p"
            },
            'start_urls': [{
                'url': 'http://foo.bar/api',
                'tags': ["test"]
            }]
        })

        strategy.dom = lxml.html.fromstring("""
        <html><body>
         <h1>Foo</h1>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom("http://foo.bar/api/test")

        # Then
        assert actual[0]['tags'] == ["test"]

    def test_regex_start_urls(self):
        # Given
        # Stub ENV variables read by ConfigLoader
        strategy = get_strategy({
            'start_urls': [
                {
                    'url': 'http://foo.bar/.*',
                    'tags': ["test"]
                }
            ],
            'selectors': {
                "lvl0": "h1",
                "lvl1": "h2",
                "lvl2": "h3",
                "content": "p"
            }
        })

        strategy.dom = lxml.html.fromstring("""
        <html><body>
         <h1>Foo</h1>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom("http://foo.bar/api/test")

        # Then
        assert actual[0]['tags'] == ["test"]
