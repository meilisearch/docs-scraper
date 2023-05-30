# coding: utf-8

EXIT_CODE_WRONG_CONFIG = 5
"""
Load the config json file.
"""

from collections import OrderedDict
import json
import os
import copy

from .version import qualified_version
from .config_validator import ConfigValidator
from .urls_parser import UrlsParser
from .selectors_parser import SelectorsParser
from .browser_handler import BrowserHandler


class ConfigLoader:
    """
    ConfigLoader
    """
    # We define them here so the linters/autocomplete know what to expect
    allowed_domains = None
    api_key = None
    app_id = None
    custom_settings = {}
    extra_records = []
    index_uid = None
    index_uid_tmp = None
    js_wait = 0
    js_render = False
    keep_tags = []
    min_indexed_level = 0
    remove_get_params = False
    scrap_start_urls = True
    scrape_start_urls = True
    selectors = None
    selectors_exclude = []
    start_urls = []
    stop_urls = []
    stop_content = []
    strategy = 'default'
    strict_redirect = True
    strip_chars = ".,;:§¶"
    use_anchors = False
    user_agent = qualified_version()
    only_content_level = False
    query_rules = []

    # data storage, starting here attribute are not config params
    config_file = None
    config_content = None
    config_original_content = None

    driver = None

    sitemap_alternate_links = False
    sitemap_urls = []
    sitemap_urls_regexs = []
    force_sitemap_urls_crawling = False

    nb_hits_max = 6000000

    def __init__(self, config):
        data = self._load_config(config)

        # Fill self from config
        for key, value in list(data.items()):
            setattr(self, key, value)

        # Start browser if needed
        self.driver = BrowserHandler.init(self.config_original_content,
                                          self.js_render,
                                          self.user_agent)

        # Validate
        ConfigValidator(self).validate()

        # Modify
        self._parse()

        # Stop browser if needed
        if not self.js_render:
            self.driver = BrowserHandler.destroy(self.driver)

        # BC new correct naming
        self.scrape_start_urls = self.scrap_start_urls if not self.scrap_start_urls else self.scrape_start_urls

    def _load_config(self, config):
        if os.path.isfile(config):
            self.config_file = config
            with open(self.config_file, mode='r', encoding='utf-8') as f:
                config = f.read()

        try:
            self.config_original_content = config
            data = json.loads(config, object_pairs_hook=OrderedDict)
            self.config_content = copy.deepcopy(data)

            return data
        except ValueError as value_error:
            raise ValueError('CONFIG is not a valid JSON') from value_error

    def _parse(self):
        # Parse Env
        self.app_id = os.environ.get('MEILISEARCH_HOST_URL', None)
        self.api_key = os.environ.get('MEILISEARCH_API_KEY', None)

        if self.index_uid_tmp is None:
            self.index_uid_tmp = os.environ.get('index_uid_TMP', self.index_uid + '_tmp')

        # Parse config
        self.selectors = SelectorsParser().parse(self.selectors)
        self.min_indexed_level = SelectorsParser().parse_min_indexed_level(
            self.min_indexed_level)
        self.start_urls = UrlsParser.parse(self.start_urls)

        # Build default allowed_domains from start_urls and stop_urls
        if self.allowed_domains is None:
            self.allowed_domains = UrlsParser.build_allowed_domains(
                self.start_urls, self.stop_urls)

    def get_extra_facets(self):
        return UrlsParser.get_extra_facets(self.start_urls)
