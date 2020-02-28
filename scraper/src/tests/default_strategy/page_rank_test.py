# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestPageRank:
    def test_default_page_rank_should_be_zero(self):
        # Given
        strategy = get_strategy({
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
        actual = strategy.get_records_from_dom()

        # Then
        assert actual[0]['weight']['page_rank'] == 0

    def test_positive_page_rank(self):
        # Given
        strategy = get_strategy({
            'start_urls': [{
                'url': 'http://foo.bar/api',
                'page_rank': 1
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
        assert actual[0]['weight']['page_rank'] == 1

    def test_positive_sub_page_page_rank(self):
        # Given
        strategy = get_strategy({
            'start_urls': [{
                'url': 'http://foo.bar/api',
                'page_rank': 1
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
        actual = strategy.get_records_from_dom("http://foo.bar/api/test")

        # Then
        assert actual[0]['weight']['page_rank'] == 1

    def test_negative_page_rank(self):
        # Given
        strategy = get_strategy({
            'start_urls': [{
                'url': 'http://foo.bar/api',
                'page_rank': -1
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
        actual = strategy.get_records_from_dom("http://foo.bar/api/test")

        # Then
        assert actual[0]['weight']['page_rank'] == -1
