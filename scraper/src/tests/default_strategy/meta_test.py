# coding: utf-8
import lxml.html
from .abstract import get_strategy


class TestMeta:
    def test_meta_number(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html>
            <header>
                <meta name="docsearch:extra" content='12'>
            </header>
            <body>
                <h1>Foo</h1>
                <p>text</p>
                <h2>Bar</h2>
                <h3>Baz</h3>
            </body>
        </html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        assert len(actual) == 4
        assert actual[0]['extra'] == 12
        assert actual[1]['extra'] == 12
        assert actual[2]['extra'] == 12
        assert actual[3]['extra'] == 12

    def test_meta_json_without_content(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
           <html>
               <header>
                   <meta name="docsearch:extra" value='["ruby","rails","python","php","symfony","javascript","java","scala","go","csharp"]'>
               </header>
               <body>
                   <h1>Foo</h1>
                   <p>text</p>
                   <h2>Bar</h2>
                   <h3>Baz</h3>
               </body>
           </html>
           """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        assert len(actual) == 4
        assert 'extra' not in actual[0]
        assert 'extra' not in actual[1]
        assert 'extra' not in actual[2]
        assert 'extra' not in actual[3]

    def test_meta_json(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
           <html>
               <header>
                   <meta name="docsearch:extra" content='["ruby","rails","python","php","symfony","javascript","java","scala","go","csharp"]'>
               </header>
               <body>
                   <h1>Foo</h1>
                   <p>text</p>
                   <h2>Bar</h2>
                   <h3>Baz</h3>
               </body>
           </html>
           """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        assert len(actual) == 4
        assert actual[0]['extra'] == ["ruby", "rails", "python", "php",
                                      "symfony", "javascript", "java", "scala",
                                      "go",
                                      "csharp"]
        assert actual[1]['extra'] == ["ruby", "rails", "python", "php",
                                      "symfony", "javascript", "java", "scala",
                                      "go",
                                      "csharp"]
        assert actual[2]['extra'] == ["ruby", "rails", "python", "php",
                                      "symfony", "javascript", "java", "scala",
                                      "go",
                                      "csharp"]
        assert actual[3]['extra'] == ["ruby", "rails", "python", "php",
                                      "symfony", "javascript", "java", "scala",
                                      "go",
                                      "csharp"]

    def test_meta_version(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html>
            <header>
                <meta name="docsearch:version" content='1.2.3'>
            </header>
            <body>
                <h1>Foo</h1>
                <p>text</p>
                <h2>Bar</h2>
                <h3>Baz</h3>
            </body>
        </html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        assert len(actual) == 4
        assert actual[0]['version'] == "1.2.3"
        assert actual[1]['version'] == "1.2.3"
        assert actual[2]['version'] == "1.2.3"
        assert actual[3]['version'] == "1.2.3"

    def test_meta_numbered_version(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html>
            <header>
                <meta name="docsearch:version" content='1.0'>
            </header>
            <body>
                <h1>Foo</h1>
                <p>text</p>
                <h2>Bar</h2>
                <h3>Baz</h3>
            </body>
        </html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        assert len(actual) == 2
        assert actual[0]['version'] == "1.0"
        assert actual[1]['version'] != 1

    def test_meta_escaped_string(self):
        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': "h1",
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': 'p'
            }
        })
        strategy.dom = lxml.html.fromstring("""
        <html>
            <header>
                <meta name="docsearch:string" content='"ok"'>
            </header>
            <body>
                <h1>Foo</h1>
                <p>text</p>
                <h2>Bar</h2>
                <h3>Baz</h3>
            </body>
        </html>
        """)

        # When
        actual = strategy.get_records_from_dom()

        # Then

        assert len(actual) == 4
        assert actual[0]['string'] == "ok"
        assert actual[1]['string'] == "ok"
        assert actual[2]['string'] == "ok"
        assert actual[3]['string'] == "ok"
