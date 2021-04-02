# coding: utf-8
import lxml.html
import pytest

from .abstract import get_strategy


class TestTags:

    @pytest.mark.parametrize('start_url, actual_url',
                             [
                                 # test_adding_tags_for_page
                                 ('http://foo.bar/api', 'http://foo.bar/api'),
                                 # test_adding_tags_for_subpage
                                 ('http://foo.bar/api', 'http://foo.bar/api/test'),
                                 # test_regex_start_urls
                                 ('http://foo.bar/*', 'http://foo.bar/api/test'),
                             ])
    def test_tags(self, start_url, actual_url):
        # Given
        strategy = get_strategy({
            'start_urls': [{
                'url': start_url,
                'tags': ['test']
            }],
            'selectors': {
                'lvl0': 'h1',
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })

        strategy.dom = lxml.html.fromstring('''
        <html><body>
         <h1>Foo</h1>
        </body></html>
        ''')

        # When
        actual = strategy.get_records_from_dom(actual_url)

        # Then
        assert actual[0]['tags'] == ['test']
