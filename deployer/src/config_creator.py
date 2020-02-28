from collections import OrderedDict
import tldextract
import re
from . import helpers
from . import helpdesk_helper
from urllib.parse import urlparse


def extract_root_from_input(input_string):
    # We cant parse the url since user might have not enter a proper link

    # We assume that the string is already the proper root
    if input_string.endswith('/'):
        return input_string
    # extracting substring before the first isolated / (not //)
    domain = re.match(".+?([^/]/(?!/))",
                      input_string)
    try:
        url_parsed = urlparse(input_string)
        # Removing unused parameters
        url_parsed._replace(params='', query='', fragment='')
        path_splited = url_parsed.path.split('/')

        # Path is redirecting to a page
        if ('html' in path_splited[-1]):
            url_parsed = url_parsed._replace(path='/'.join(path_splited[: -1]))
        # We are fine
        else:
            pass

        return url_parsed.geturl() + '/'
    except ValueError:
        return domain.group() if domain else input_string


def assert_list_non_empty(list_to_check):
    # Check if the input is not None or empty. Otherwise, it raises an exception
    if not list_to_check or len(list_to_check) == 0:
        raise Exception('{} is None or empty'.format(list_to_check))


def to_docusaurus_config(config, urls):
    assert_list_non_empty(urls)
    config["sitemap_urls"] = [
        extract_root_from_input(urls[0]) + "sitemap.xml"]
    config["sitemap_alternate_links"] = True
    config["custom_settings"] = {"attributesForFaceting": ["language",
                                                            "version"]
                                     }
    start_url = urls[0]
    if '/docs/' not in start_url:
        if not start_url.endswith('/'):
            start_url += '/'
        start_url += 'docs/'
    config["start_urls"] = [start_url]
    config["selectors"]["lvl0"] = OrderedDict((
        ("selector",
         "//*[contains(@class,'navGroups')]//*[contains(@class,'navListItemActive')]/preceding::h3[1]"),
        ("type", "xpath"),
        ("global", True),
        ("default_value", "Documentation")
    ))
    config["selectors"]["lvl1"] = ".post h1"
    config["selectors"]["lvl2"] = ".post h2"
    config["selectors"]["lvl3"] = ".post h3"
    config["selectors"]["lvl4"] = ".post h4"
    config["selectors"]["lvl5"] = ".post h5"
    config["selectors"]["text"] = ".post article p, .post article li"
    config["selectors_exclude"] = [".hash-link"]

    return config


def to_docusaurus_v2_config(config, urls):
    assert_list_non_empty(urls)
    config["sitemap_urls"] = [
        extract_root_from_input(urls[0]) + "sitemap.xml"]
    config["sitemap_alternate_links"] = True
    start_url = urls[0]
    if '/docs/' not in start_url:
        if not start_url.endswith('/'):
            start_url += '/'
        start_url += 'docs/'
    config["start_urls"] = [start_url]

    config["selectors"]["lvl0"] = OrderedDict((
        ("selector",
         ".menu__link--sublist.menu__link--active"),
        ("global", True),
        ("default_value", "Documentation")
    ))
    config["selectors"]["lvl1"] = "[class^='docItemContainer_'] h1"
    config["selectors"]["lvl2"] = "[class^='docItemContainer_'] h2"
    config["selectors"]["lvl3"] = "[class^='docItemContainer_'] h3"
    config["selectors"]["lvl4"] = "[class^='docItemContainer_'] h4"
    config["selectors"]["lvl5"] = "[class^='docItemContainer_'] h5"
    config["selectors"]["text"] = "[class^='docItemContainer_'] p, [class^='docItemContainer_'] li"
    config["selectors_exclude"] = [".hash-link"]

    return config


def to_gitbook_config(config):
    config["selectors"]["lvl0"] = ".markdown-section h1"
    config["selectors"]["lvl1"] = ".markdown-section h2"
    config["selectors"]["lvl2"] = ".markdown-section h3"
    config["selectors"]["lvl3"] = ".markdown-section h4"
    config["selectors"]["lvl4"] = ".markdown-section h4"
    config["selectors"]["lvl5"] = ".markdown-section h5"
    config["selectors"]["text"] = ".markdown-section p, .markdown-section li"

    return config


def to_pkgdown_config(config, urls=None):
    if urls:
        root = extract_root_from_input(urls[0])
        config["start_urls"] = [{
            "url": root + "index.html",
            "selectors_key": "homepage",
            "tags": [
                "homepage"
            ]
        },
            {
                "url": root + "reference",
                "selectors_key": "reference",
                "tags": [
                    "reference"
                ]
            },
            {
                "url": root + "articles",
                "selectors_key": "articles",
                "tags": [
                    "articles"
                ]
            }]

        config["sitemap_urls"] = [
            root + "sitemap.xml"]

    config["selectors"] = OrderedDict((
        ("homepage", OrderedDict((
            ("lvl0", OrderedDict((
                ("selector", ".contents h1"),
                ("default_value", "pkgdown Home page")
            ))),
            ("lvl1", ".contents h2"),
            ("lvl2", OrderedDict((
                ("selector", ".contents h3"),
                ("default_value", "Context")
            ))),
            ("lvl3", ".ref-arguments td, .ref-description"),
            ("text", ".contents p, .contents li, .contents .pre")
        ))),
        ("reference", OrderedDict((
            ("lvl0", ".contents h1"),
            ("lvl1", OrderedDict((
                ("selector", ".contents .name"),
                ("default_value", "Argument")
            ))),
            ("lvl2", OrderedDict((
                ("selector", ".ref-arguments th"),
                ("default_value", "Description")
            ))),
            ("lvl3", ".ref-arguments td, .ref-description"),
            ("text", ".contents p, .contents li")
        ))),
        ("articles", OrderedDict((
            ("lvl0", ".contents h1"),
            ("lvl1", ".contents .name"),
            ("lvl2", OrderedDict((
                ("selector", ".contents h2, .contents h3"),
                ("default_value", "Context")
            ))),
            ("text",
             ".contents p, .contents li")
        ))),
        ("default", OrderedDict((
            ("lvl1", ".contents h2"),
            ("lvl2", ".contents h3, .contents th"),
            ("lvl3", ".contents h4"),
            ("lvl4", ".contents h5"),
            ("text",
             ".contents p, .contents li, .usage, .template-article .contents .pre")
        )))
    ))
    config["selectors_exclude"] = [".dont-index"]
    config["stop_urls"] = ["/reference/$",
                           "/reference/index.html",
                           "/articles/$",
                           "/articles/index.html"]
    config["custom_settings"] = {
        "separatorsToIndex": "_",
        "attributesToRetrieve": ["hierarchy",
                                 "content", "anchor", "url",
                                 "url_without_anchor"]
    }
    config["min_indexed_level"] = 2
    return config


def to_vuepress_config(config):
    config["selectors"]["lvl0"] = OrderedDict((
        ("selector", "p.sidebar-heading.open"),
        ("global", True),
        ("default_value", "Documentation")
    ))
    config["custom_settings"] = {"attributesForFaceting": ["lang"]
                                 }
    config["selectors"]["lvl1"] = ".theme-default-content h1"
    config["selectors"]["lvl2"] = ".theme-default-content h2"
    config["selectors"]["lvl3"] = ".theme-default-content h3"
    config["selectors"]["lvl4"] = ".theme-default-content h4"
    config["selectors"]["lvl5"] = ".theme-default-content h5"
    config["selectors"]["text"] = ".theme-default-content p, .theme-default-content li"
    config["selectors"]["lang"] = OrderedDict((
        ("selector", "/html/@lang"),
        ("type", "xpath"),
        ("global", True),
        ("default_value", "en-US")
    ))
    config["selectors_exclude"] = [".table-of-contents"]

    config["scrap_start_urls"] = False
    config["strip_chars"] = " .,;:#"

    return config


def to_larecipe_config(config, urls=None):
    if urls:
        config["sitemap_urls"] = [
            extract_root_from_input(urls[0]) + "sitemap.xml"]
    config["selectors"]["lvl0"] = OrderedDict((
        ("selector",
         "//div[contains(@class, 'sidebar')]//li/a[text()=//div[contains(@class, 'article')]//h1[1]/text()]"),
        ("global", True),
        ("type", "xpath"),
        ("default_value", "Documentation")
    ))

    config["selectors"]["lvl1"] = "div.article h1"
    config["selectors"]["lvl2"] = "div.article h2"
    config["selectors"]["lvl3"] = "div.article h3"
    config["selectors"]["lvl4"] = "div.article h4"
    config["selectors"]["lvl5"] = "div.article h5"
    config["selectors"]["text"] = "div.article p, div.article li"

    return config


def to_publii_config(config, urls=None):
    if urls:
        config["sitemap_urls"] = [
            extract_root_from_input(urls[0]) + "sitemap.xml"]

    config["selectors"]["lvl0"] = OrderedDict((
        ("selector", ".active-parent > span"),
        ("global", True),
        ("default_value", "Documentation")
    ))

    config["selectors"]["lvl1"] = ".content h1"
    config["selectors"]["lvl2"] = ".content h2"
    config["selectors"]["lvl3"] = ".content h3"
    config["selectors"]["lvl4"] = ".content h4"
    config["selectors"]["lvl5"] = ".content h5"
    config["selectors"]["text"] = ".content p, .content li"
    config["only_content_level"] = True

    return config


def to_jsdoc_config(config):
    config["stop_urls"] = ["\\.js\\.html",
                           "/index\\.html$"]

    config["selectors"]["lvl0"] = OrderedDict((
        ("selector", "#main .page-title"),
        ("global", True),
        ("default_value", "Documentation")
    ))

    config["selectors"]["lvl1"] = "#main h3"
    config["selectors"]["lvl2"] = "#main h4"
    config["selectors"]["lvl3"] = "#main h5"
    config["selectors"]["lvl4"] = "#main h6, #main td.name"
    del config["selectors"]["lvl5"]
    config["selectors"]["text"] = "#main p, #main li"
    config["selectors_exclude"] = [".signature",
                                   ".type-signature",
                                   ".details"]

    return config


def create_config(u=None):
    config = OrderedDict((
        ("index_name", ""),
        ("start_urls", []),
        ("stop_urls", []),
        ("selectors", OrderedDict((
            ("lvl0", "FIXME h1"),
            ("lvl1", "FIXME h2"),
            ("lvl2", "FIXME h3"),
            ("lvl3", "FIXME h4"),
            ("lvl4", "FIXME h5"),
            ("lvl5", "FIXME h6"),
            ("text", "FIXME p, FIXME li")
        )))
    ))

    if u is None:
        u = helpers.get_user_value("start url: ")

    urls = [u]

    if helpdesk_helper.is_helpdesk_url(u):
        cuid = helpdesk_helper.get_conversation_ID_from_url(u)

        conversation = helpdesk_helper.get_conversation(cuid)
        conversation_with_threads = helpdesk_helper.get_conversation_with_threads(cuid)
        url_from_conversation = helpdesk_helper.get_start_url_from_conversation(
            conversation_with_threads)
        urls = [url_from_conversation]
        u = url_from_conversation

        if helpdesk_helper.is_docusaurus_conversation(conversation):
            config = to_docusaurus_config(config, urls)
        elif helpdesk_helper.is_docusaurus_v2_conversation(conversation):
            config = to_docusaurus_v2_config(config, urls)
        elif helpdesk_helper.is_gitbook_conversation(conversation):
            config = to_gitbook_config(config)
        elif helpdesk_helper.is_pkgdown_conversation(conversation):
            config = to_pkgdown_config(config, urls)
        elif helpdesk_helper.is_vuepress_conversation(conversation):
            config = to_vuepress_config(config)
        elif helpdesk_helper.is_larecipe_conversation(conversation):
            config = to_larecipe_config(config, urls)
        elif helpdesk_helper.is_publii_conversation(conversation):
            config = to_publii_config(config, urls)
        elif helpdesk_helper.is_jsdoc_conversation(conversation):
            config = to_jsdoc_config(config)

        config["conversation_id"] = [cuid]

    if '.html' in u:
        urls.append(u.rsplit('/', 1)[0])

    # Use subdomain for github website https://<subdomain>.github.io/
    config['index_name'] = tldextract.extract(
        u).subdomain if tldextract.extract(
        u).domain == 'github' else tldextract.extract(u).domain

    if len(config['start_urls']) == 0:
        config['start_urls'] = urls

    user_index_name = helpers.get_user_value(
        'index_name is \033[1;33m{}\033[0m [enter to confirm]: '.format(config[
            "index_name"]))

    if user_index_name != "":
        config['index_name'] = user_index_name
        print('index_name is now \033[1;33m{}\033[0m'.format(config[
            "index_name"]))

    return config
