# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestCustomAttributes:
    def test_simple(self):
        # Given

        selectors = {
            "lvl0": "h1",
            "lvl1": {
                "selector": ".parameters",
                "attributes": {
                    "name": ".name",
                    "custom_description": {
                        "selector": "//div[contains(@class, 'parameters')]/div[contains(@class,'description')]",
                        "type": "xpath"
                    }
                }
            },
            "content": "p"
        }

        strategy = get_strategy({"selectors": selectors})
        strategy.dom = lxml.html.fromstring("""
           <html><body>
             <h1>Foo</h1>
             <div class='parameters'>
                <div class="name">Foo</div>
                <div class="description">Bar</div>
             </div>
             <p>Baz</p>
           </body></html>
           """)

        # When
        actual = strategy.get_records_from_dom()

        # Then
        assert len(actual) == 3
        assert actual[0]['hierarchy']['lvl0'] == 'Foo'
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None

        assert actual[1]['hierarchy']['lvl0'] == 'Foo'
        assert type(actual[1]['hierarchy']['lvl1']) is dict
        assert actual[1]['hierarchy']['lvl1']['name'] == 'Foo'
        assert actual[1]['hierarchy']['lvl1']['custom_description'] == 'Bar'
        assert actual[1]['hierarchy']['lvl2'] is None

        assert actual[2]['hierarchy']['lvl0'] == 'Foo'
        assert type(actual[2]['hierarchy']['lvl1']) is dict
        assert actual[2]['content'] == 'Baz'
