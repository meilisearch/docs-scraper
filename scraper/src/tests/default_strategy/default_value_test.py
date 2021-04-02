# coding: utf-8
import lxml.html
import pytest

from .abstract import get_strategy


@pytest.fixture
def get_selectors_lvl0():
    selectors_lvl0_variants = {
        'default_value': {
            'selector': 'h1',
            'default_value': 'Documentation'
        },
        'default_value_for_text': 'h1',
        'default_value_with_global': {
            'selector': 'h1',
            'global': True,
            'default_value': 'Documentation'
        },
        'default_value_should_not_override': {
            'selector': 'h1',
            'global': True,
            'default_value': 'Documentation'
        },
        "default_value_empty": {
            'selector': 'h1',
            'default_value': 'Documentation'
        },
        'default_value_empty_and_global': {
            'selector': 'h1',
            'global': 'true',
            'default_value': 'Documentation'
        },
    }

    def _get_selector_lvl0(test_type):
        return selectors_lvl0_variants.get(test_type)

    return _get_selector_lvl0


@pytest.fixture
def get_selectors_content():
    selectors_content_variants = {
        'default_value': 'p',
        'default_value_for_text': {
            'selector': 'p',
            'default_value': 'Documentation'
        },
        'default_value_with_global': 'p',
        'default_value_should_not_override': 'p',
        "default_value_empty": 'p',
        'default_value_empty_and_global': 'p',
    }

    def _get_selector_content(test_type):
        return selectors_content_variants.get(test_type)

    return _get_selector_content


@pytest.fixture
def get_strategy_dom():
    strategy_dom_variants = {
        'default_value': """
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """,
        'default_value_for_text': """
        <html><body>
            <h1>Foo</h1>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """,
        'default_value_with_global': """
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """,
        'default_value_should_not_override': """
        <html><body>
            <h1>Foo</h1>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """,
        "default_value_empty": """
        <html><body>
            <h1></h1>
            <p>text</p>git
            <h2>Bar</h2>
            <h3>Baz</h3>
        </body></html>
        """,
        'default_value_empty_and_global': """
        <html><body>
            <p>text</p>
            <h2>Bar</h2>
            <h3>Baz</h3>
            <h1></h1>
        </body></html>
        """,
    }

    def _get_strategy_dom(test_type):
        return strategy_dom_variants.get(test_type)

    return _get_strategy_dom


@pytest.fixture
def get_actual_type():
    actual_type_variants = {
        'default_value': 'content',
        'default_value_for_text': 'lvl0',
        'default_value_with_global': 'content',
        'default_value_should_not_override': 'content',
        "default_value_empty": 'lvl0',
        'default_value_empty_and_global': 'content',
    }

    def _get_actual_type(test_type):
        return actual_type_variants.get(test_type)

    return _get_actual_type


@pytest.fixture
def get_actual_lvl0():
    actual_lvl0_variants = {
        'default_value': 'Documentation',
        'default_value_for_text': 'Foo',
        'default_value_with_global': 'Documentation',
        'default_value_should_not_override': 'Foo',
        "default_value_empty": 'Documentation',
        'default_value_empty_and_global': 'Documentation',
    }

    def _get_actual_lvl0(test_type):
        return actual_lvl0_variants.get(test_type)

    return _get_actual_lvl0


@pytest.fixture
def get_actual_content():
    actual_content_variants = {
        'default_value': 'text',
        'default_value_for_text': 'Documentation',
        'default_value_with_global': 'text',
        'default_value_should_not_override': 'text',
        "default_value_empty": None,
        'default_value_empty_and_global': 'text',
    }

    def _get_actual_content(test_type):
        return actual_content_variants.get(test_type)

    return _get_actual_content


@pytest.fixture
def get_actual_len():
    actual_len_variants = {
        'default_value': 3,
        'default_value_for_text': 3,
        'default_value_with_global': 3,
        'default_value_should_not_override': 3,
        "default_value_empty": 4,
        'default_value_empty_and_global': 3,
    }

    def _get_actual_len(test_type):
        return actual_len_variants.get(test_type)

    return _get_actual_len


class TestGetRecordsFromDomWithDefaultValue:

    @pytest.mark.parametrize('test_type',
                             [
                                 ('default_value'),
                                 ('default_value_for_text'),
                                 ('default_value_with_global'),
                                 ('default_value_should_not_override'),
                                 ('default_value_empty'),
                                 ('default_value_empty_and_global'),
                             ])
    def test_default(self,
                     get_selectors_lvl0,
                     get_selectors_content,
                     get_strategy_dom,
                     get_actual_len,
                     get_actual_type,
                     get_actual_lvl0,
                     get_actual_content,
                     test_type):

        # Given
        strategy = get_strategy({
            'selectors': {
                'lvl0': get_selectors_lvl0(test_type),
                'lvl1': 'h2',
                'lvl2': 'h3',
                'content': get_selectors_content(test_type)
            }
        })
        strategy.dom = lxml.html.fromstring(get_strategy_dom(test_type))

        # When
        actual = strategy.get_records_from_dom()

        # Then

        # First record has the global H1
        assert len(actual) == get_actual_len(test_type)
        assert actual[0]['type'] == get_actual_type(test_type)
        assert actual[0]['hierarchy']['lvl0'] == get_actual_lvl0(test_type)
        assert actual[0]['hierarchy']['lvl1'] is None
        assert actual[0]['hierarchy']['lvl2'] is None
        assert actual[0]['content'] == get_actual_content(test_type)
