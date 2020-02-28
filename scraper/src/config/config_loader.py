# coding: utf-8

EXIT_CODE_WRONG_CONFIG = 5
"""
Load the config json file.
"""

from collections import OrderedDict
from distutils.util import strtobool
import json
import os
import copy

from .config_validator import ConfigValidator
from .nb_hits_updater import NbHitsUpdater
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
    custom_settings = None
    extra_records = []
    index_name = None
    index_name_tmp = None
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
    strip_chars = u".,;:§¶"
    update_nb_hits = None
    use_anchors = False
    user_agent = 'Algolia DocSearch Crawler'
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
            with open(self.config_file, 'r') as f:
                config = f.read()

        try:
            self.config_original_content = config
            data = json.loads(config, object_pairs_hook=OrderedDict)
            self.config_content = copy.deepcopy(data)

            return data
        except ValueError:
            raise ValueError('CONFIG is not a valid JSON')
            exit(EXIT_CODE_WRONG_CONFIG)

    def _parse(self):
        # Parse Env
        self.app_id = os.environ.get('APPLICATION_ID', None)
        self.api_key = os.environ.get('API_KEY', None)
        self.update_nb_hits = os.environ.get('UPDATE_NB_HITS', None)
        if self.update_nb_hits is not None:
            self.update_nb_hits = bool(strtobool(self.update_nb_hits))
        if self.index_name_tmp is None:
            self.index_name_tmp = os.environ.get('INDEX_NAME_TMP', self.index_name + '_tmp')

        # Parse config
        self.selectors = SelectorsParser().parse(self.selectors)
        self.min_indexed_level = SelectorsParser().parse_min_indexed_level(
            self.min_indexed_level)
        self.start_urls = UrlsParser.parse(self.start_urls)

        # Build default allowed_domains from start_urls and stop_urls
        if self.allowed_domains is None:
            self.allowed_domains = UrlsParser.build_allowed_domains(
                self.start_urls, self.stop_urls)

    def update_nb_hits_value(self, nb_hits):
        if self.config_file is not None:
            # config loaded from file
            previous_nb_hits = None if 'nb_hits' not in self.config_content else \
                self.config_content['nb_hits']
            nb_hit_updater = NbHitsUpdater(self.config_file,
                                           self.config_content,
                                           previous_nb_hits, nb_hits)
            nb_hit_updater.update(self.update_nb_hits)

    def get_extra_facets(self):
        return UrlsParser.get_extra_facets(self.start_urls)
