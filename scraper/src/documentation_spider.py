"""
DocumentationSpider
"""
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

# Import for the sitemap behavior
from scrapy.spiders import SitemapSpider
from scrapy.spiders.sitemap import regex
import re
import os

# End of import for the sitemap behavior

from scrapy.spidermiddlewares.httperror import HttpError

from scrapy.exceptions import CloseSpider

EXIT_CODE_EXCEEDED_RECORDS = 4


class DocumentationSpider(CrawlSpider, SitemapSpider):
    """
    DocumentationSpider
    """
    http_user = os.environ.get('DOCSEARCH_BASICAUTH_USERNAME', None)
    http_pass = os.environ.get('DOCSEARCH_BASICAUTH_PASSWORD', None)
    meilisearch_helper = None
    strategy = None
    js_render = False
    js_wait = 0
    match_capture_any_scheme = re.compile(r"^(https?)(.*)")
    backreference_any_scheme = r"^https?\2(.*)$"
    # Could be any url prefix such as http://www or http://
    every_schemes = ["http", "https"]
    reason_to_stop = None

    @staticmethod
    def to_any_scheme(url):
        """Return a regex that represent the URL and match any scheme from it"""
        return url if not re.match(
            DocumentationSpider.match_capture_any_scheme, url) else re.sub(
            DocumentationSpider.match_capture_any_scheme,
            DocumentationSpider.backreference_any_scheme, url)

    @staticmethod
    def to_other_scheme(url):
        """Return a list with the translation to this url into each other scheme."""
        other_scheme_urls = []
        match = DocumentationSpider.match_capture_any_scheme.match(url)
        assert match
        if not (match and match.group(1) and match.group(2)):
            raise ValueError(
                "Must have a match and split the url into the scheme and the rest. url: " + url)

        previous_scheme = match.group(1)
        url_with_no_scheme = match.group(2)

        for scheme in DocumentationSpider.every_schemes:
            if scheme != previous_scheme:
                other_scheme_urls.append(scheme + url_with_no_scheme)
        return other_scheme_urls

    def __init__(self, config, meilisearch_helper, strategy, *args, **kwargs):
        # Scrapy config
        self.name = config.index_name
        self.allowed_domains = config.allowed_domains
        self.start_urls_full = config.start_urls
        self.start_urls = [start_url['url'] for start_url in config.start_urls]
        # We need to ensure that the stop urls are scheme agnostic too if it represents URL
        self.stop_urls = [DocumentationSpider.to_any_scheme(stop_url) for
                          stop_url in config.stop_urls]
        self.meilisearch_helper = meilisearch_helper
        self.strategy = strategy
        self.js_render = config.js_render
        self.js_wait = config.js_wait
        self.scrape_start_urls = config.scrape_start_urls
        self.remove_get_params = config.remove_get_params
        self.strict_redirect = config.strict_redirect
        self.nb_hits_max = config.nb_hits_max
        super(DocumentationSpider, self).__init__(*args, **kwargs)

        # Get rid of scheme consideration
        # Start_urls must stays authentic URL in order to be reached, we build agnostic scheme regex based on those URL
        start_urls_any_scheme = [DocumentationSpider.to_any_scheme(start_url)
                                 for start_url in self.start_urls]
        link_extractor = LxmlLinkExtractor(
            allow=start_urls_any_scheme,
            deny=self.stop_urls,
            tags=('a', 'area', 'iframe'),
            attrs=('href', 'src'),
            canonicalize=(not config.js_render or not config.use_anchors)
        )

        DocumentationSpider.rules = [
            Rule(link_extractor, callback=self.parse_from_start_url,
                 follow=True),
        ]

        # START _init_ part from SitemapSpider
        # We son't want to check anything if we don't even have a sitemap URL
        if config.sitemap_urls:
            # In case we don't have a special documentation regex,
            # we assume that start_urls are there to match a documentation part
            self.sitemap_urls_regexs =\
                config.sitemap_urls_regexs if config.sitemap_urls_regexs else start_urls_any_scheme

            sitemap_rules = []
            if self.sitemap_urls_regexs:
                for regex in self.sitemap_urls_regexs:
                    sitemap_rules.append((regex, 'parse_from_sitemap'))
            else:  # Neither start url nor regex: default, we parse all
                print("Neither start url nor regex: default, we scrap all")
                sitemap_rules = [('.*', 'parse_from_sitemap')]

            self.__init_sitemap_(config.sitemap_urls, sitemap_rules,
                                 config.sitemap_alternate_links)
            self.force_sitemap_urls_crawling = config.force_sitemap_urls_crawling

        # END _init_ part from SitemapSpider
        super(DocumentationSpider, self)._compile_rules()

    def start_requests(self):
        # We crawl according to the sitemap
        for url in self.sitemap_urls:
            yield Request(url, callback=self._parse_sitemap,
                          meta={
                              "alternative_links": DocumentationSpider.to_other_scheme(
                                  url)
                          },
                          errback=self.errback_alternative_link)
        # Redirection is neither an error (4XX status) nor a success (2XX) if dont_redirect=False, thus we force it

        # We crawl the start URL in order to ensure we didn't miss anything (Even if we used the sitemap)
        for url in self.start_urls:
            yield Request(url,
                          callback=self.parse_from_start_url if self.scrape_start_urls else self.parse,
                          # If we wan't to crawl (default behavior) without scraping, we still need to let the
                          # crawling spider acknowledge the content by parsing it with the built-in method
                          meta={
                              "alternative_links": DocumentationSpider.to_other_scheme(
                                  url)
                          },
                          errback=self.errback_alternative_link)

    def add_records(self, response, from_sitemap):
        records = self.strategy.get_records_from_response(response)
        self.meilisearch_helper.add_records(records, response.url, from_sitemap)

        DocumentationSpider.NB_INDEXED += len(records)

        # Arbitrary limit
        if self.nb_hits_max > 0 and DocumentationSpider.NB_INDEXED > self.nb_hits_max:
            DocumentationSpider.NB_INDEXED = 0
            self.reason_to_stop = "Too much hits, DocSearch only handle {} records".format(
                int(self.nb_hits_max))
            raise ValueError(self.reason_to_stop)
            exit(EXIT_CODE_EXCEEDED_RECORDS)

    def parse_from_sitemap(self, response):
        if self.reason_to_stop is not None:
            raise CloseSpider(reason=self.reason_to_stop)

        if (not self.force_sitemap_urls_crawling) and (
                not self.is_rules_compliant(response)):
            print("\033[94m> Ignored from sitemap:\033[0m " + response.url)
        else:
            self.add_records(response, from_sitemap=True)
            # We don't return self.parse(response) in order to avoid crawling those web page

    def parse_from_start_url(self, response):
        if self.reason_to_stop is not None:
            raise CloseSpider(reason=self.reason_to_stop)

        if self.is_rules_compliant(response):
            self.add_records(response, from_sitemap=False)

        else:
            print("\033[94m> Ignored: from start url\033[0m " + response.url)

        return self.parse(response)

    def is_rules_compliant(self, response):

        # Even if the link extract were compliant, we may have been redirected. Hence we check a new time

        # Redirection redirect on a start url
        if not self.scrape_start_urls and (
                response.url in self.start_urls or response.request.url in self.start_urls):
            return False

        for rule in self._rules:
            if not self.strict_redirect:
                if rule.link_extractor._link_allowed(response):
                    continue

                if rule.link_extractor._link_allowed(response.request):
                    response.replace(url=response.request.url)
                    continue
            else:
                if rule.link_extractor._link_allowed(
                        response) and rule.link_extractor._link_allowed(
                    response.request):
                    continue
            return False

        return True

    def errback_alternative_link(self, failure):
        """
        This error callback will launch the same request with the alternative_links if there are some left
        Only for start_urls and sitemap_urls
        """
        if hasattr(failure.value, 'response'):
            if hasattr(failure.value.response, 'status'):
                self.logger.error('Http Status:%s on %s',
                                  failure.value.response.status,
                                  failure.value.response.url)
            else:
                self.logger.error('Failure : %s', failure.value)

        else:
            self.logger.error('Failure without response %s', failure.value)

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            meta = failure.request.meta
            meta["alternative_fallback"] = True

            if len(meta["alternative_links"]) > 0:
                alternative_link = meta["alternative_links"].pop(0)
                self.logger.error('Alternative link: %s', alternative_link)
                yield failure.request.replace(
                    url=alternative_link,
                    meta=meta
                )

                # Other check available such as DNSLookupError, TimeoutError, TCPTimedOutError)...

    def __init_sitemap_(self, sitemap_urls, custom_sitemap_rules,
                        sitemap_alternate_links):
        """Init method of a SiteMapSpider @Scrapy"""
        self.sitemap_alternate_links = sitemap_alternate_links
        self.sitemap_urls = sitemap_urls
        self.sitemap_rules = custom_sitemap_rules
        self._cbs = []
        for r, c in self.sitemap_rules:
            if isinstance(c, str):
                c = getattr(self, c)
            self._cbs.append((regex(r), c))
        self._follow = [regex(x) for x in self.sitemap_follow]
