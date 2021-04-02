# coding: utf-8
import lxml.html
import pytest

from .abstract import get_strategy


class TestPageRank:

    @pytest.mark.parametrize('page_rank, page_url',
                             [
                                 # test_default_page_rank_should_be_zero
                                 (0, ''),
                                 # test_positive_page_rank
                                 (1, 'http://foo.bar/api'),
                                 # test_positive_sub_page_page_rank
                                 (1, 'http://foo.bar/api/test'),
                                 # test_negative_page_rank
                                 (-1, 'http://foo.bar/api/test'),
                             ])
    def test_page_rank(self, page_rank, page_url):
        # Given
        if page_rank == 0:
            strategy = get_strategy({
                'selectors': {
                    "lvl0": "h1",
                    "lvl1": "h2",
                    "lvl2": "h3",
                    "content": "p"
                }
            })
        else:
            strategy = get_strategy({
                'start_urls': [{
                    'url': 'http://foo.bar/api',
                    'page_rank': page_rank
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
        actual = strategy.get_records_from_dom(page_url)

        # Then
        assert actual[0]['weight']['page_rank'] == page_rank
