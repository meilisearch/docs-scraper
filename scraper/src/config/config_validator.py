

import builtins


class ConfigValidator:
    config = None

    def __init__(self, config):
        self.config = config

    def validate(self):
        """Check for all needed parameters in config"""
        if not self.config.index_uid:
            raise ValueError('index_uid is not defined')

        # Start_urls is mandatory
        if not self.config.start_urls and not self.config.sitemap_urls:
            raise ValueError('start_urls is not defined, nor sitemap urls')

        # Start urls must be an array
        if self.config.start_urls and not isinstance(self.config.start_urls,
                                                     list):
            raise builtins.Exception('start_urls should be list')

        # Stop urls must be an array
        if self.config.stop_urls and not isinstance(self.config.stop_urls,
                                                    list):
            raise builtins.Exception('stop_urls should be list')

        # Custom settings must be a dict
        if self.config.custom_settings and not isinstance(self.config.custom_settings,
                                                    dict):
            raise builtins.Exception('custom_settings must be a dictionary')

        if self.config.js_render and not isinstance(self.config.js_render,
                                                    bool):
            raise builtins.Exception('js_render should be boolean')

        # `js_wait` is set to 0s by default unless it is specified
        if self.config.js_wait and not isinstance(self.config.js_wait, int):
            raise builtins.Exception('js_wait should be integer')

        if self.config.use_anchors and not isinstance(self.config.use_anchors,
                                                      bool):
            raise builtins.Exception('use_anchors should be boolean')

        if self.config.sitemap_alternate_links and not isinstance(
                self.config.sitemap_alternate_links, bool):
            raise builtins.Exception('sitemap_alternate_links should be boolean')

        if self.config.sitemap_urls_regexs and not self.config.sitemap_urls:
            raise builtins.Exception(
                'You gave an regex to parse sitemap but you didn\'t provide a sitemap url')

        if self.config.sitemap_urls_regexs and not self.config.sitemap_urls:
            for regex in self.config.sitemap_urls_regex:
                if not isinstance(regex, str):
                    raise builtins.Exception(
                        'You gave an bad regex: ' + regex + ' must be a string')

        if self.config.force_sitemap_urls_crawling and not self.config.sitemap_urls:
            raise builtins.Exception(
                'You want to force the sitemap crawling but you didn\'t provide a sitemap url')

        if not self.config.scrape_start_urls and not self.config.scrap_start_urls:
            raise builtins.Exception(
                'Please use only the new variable name: scrape_start_urls')

        if self.config.nb_hits_max and not isinstance(self.config.nb_hits_max,
                                                      int):
            raise builtins.Exception('nb_hits_max should be integer')
