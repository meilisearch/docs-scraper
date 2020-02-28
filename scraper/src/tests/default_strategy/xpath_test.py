# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestGetRecordsFromDomWithXpath:
    def test_one_xpath(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector':
                        "descendant-or-self::"
                        "*[@class and contains(concat(' ', normalize-space(@class), ' '), ' title ')]",
                    'type': 'xpath'
                },
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <h1 class="title">Foo</h1>
            <p>text</p>
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
        assert actual[0]['hierarchy']['lvl0'] == 'Foo'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] is None

    def test_two_xpath_including_one_global(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector':
                        "descendant-or-self::"
                        "*[@class and contains(concat(' ', normalize-space(@class), ' '), ' title ')]",
                    'type': 'xpath',
                    'global': True
                },
                'lvl1': {
                    'selector':
                        "descendant-or-self::"
                        "*[@class and contains(concat(' ', normalize-space(@class), ' '), ' subtitle ')]",
                    'type': 'xpath'
                },
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h2 class="subtitle">Bar</h2>
            <h3>Baz</h3>
            <h1 class="title">Foo</h1>
            <h1 class="title">Foo</h1>
        </body></html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        # First record has the global H1
        assert len(actual) == 3
        assert actual[0]['type'] == 'content'
        assert actual[0]['hierarchy']['lvl0'] == 'Foo Foo'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == 'text'

        assert actual[1]['type'] == 'lvl1'
        assert actual[1]['hierarchy']['lvl0'] == 'Foo Foo'
        assert actual[1]['hierarchy']['lvl1'] == 'Bar'
        assert actual[1]['hierarchy']['lvl2'] is None
        assert actual[1]['content'] is None

    def test_select_parent_with_xpath(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': {
                    'selector': '//li[@class="active"]/../../../*[@class="title"]',
                    'type': 'xpath',
                    'global': True
                },
                'lvl1': 'li.active',
                'lvl2': 'h3',
                'content': 'p'
            }
        })

        strategy.dom = lxml.html.fromstring("""
        <html><body>
            <p>text</p>
            <h3>Baz</h3>
            <div>
                <h1 class="title">Foo</h1>
                <div>
                    <ul>
                        <li class="active">Bar</li>
                        <li>Bar 2</li>
                    </ul>
                </div>
            </div>
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
