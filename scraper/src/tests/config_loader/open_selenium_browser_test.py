# coding: utf-8
from ...config.config_loader import ConfigLoader
from ...config.browser_handler import BrowserHandler
from .abstract import config


class TestOpenSeleniumBrowser:
    def test_browser_not_needed_by_default(self):
        c = config()

        actual = ConfigLoader(c)

        assert BrowserHandler.conf_need_browser(actual.config_original_content,
                                                actual.js_render) is False

    def test_browser_needed_when_js_render_true(self, monkeypatch):
        from .mocked_init import MockedInit
        monkeypatch.setattr("selenium.webdriver.chrome",
                            lambda x: MockedInit())
        monkeypatch.setattr("time.sleep", lambda x: "")
        # When
        c = config({
            "js_render": True
        })

        actual = ConfigLoader(c)

        assert BrowserHandler.conf_need_browser(actual.config_original_content,
                                                actual.js_render) is True

    def test_browser_needed_when_config_contains_automatic_tag(self,
                                                               monkeypatch):
        from .mocked_init import MockedInit
        monkeypatch.setattr("selenium.webdriver.chrome",
                            lambda x: MockedInit())
        monkeypatch.setattr("time.sleep", lambda x: "")

        # When
        c = config({
            "start_urls": [
                {
                    "url": "https://symfony.com/doc/(?P<version>.*?)/(?P<type_of_content>.*?)/",
                    "variables": {
                        "version": {
                            "url": "https://symfony.com/doc/current/book/controller.html",
                            "js": """\
var versions = $('.doc-switcher .versions li').map(function (i, elt) {\
  return $(elt).find('a').html().split('/')[0].replace(/ |\\n/g,'');\
}).toArray();\
versions.push('current');\
return JSON.stringify(versions);"""
                        },
                        "type_of_content": ["book", "bundles", "reference",
                                            "components", "cookbook",
                                            "best_practices"]
                    }
                }
            ]
        })

        actual = ConfigLoader(c)

        assert BrowserHandler.conf_need_browser(actual.config_original_content,
                                                actual.js_render) is True
