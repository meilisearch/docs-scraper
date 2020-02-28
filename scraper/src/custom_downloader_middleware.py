"""
CustomDownloaderMiddleware
"""

import time

from scrapy.http import HtmlResponse
from urllib.parse import urlparse, unquote_plus


class CustomDownloaderMiddleware:
    driver = None

    def __init__(self):
        self.seen = {}  # TODO could be removed
        self.driver = CustomDownloaderMiddleware.driver

    def process_request(self, request, spider):
        if not spider.js_render:
            return None

        if spider.remove_get_params:
            o = urlparse(request.url)
            url_without_params = o.scheme + "://" + o.netloc + o.path
            request = request.replace(url=url_without_params)

        if request.url in self.seen:
            return None

        self.seen[request.url] = True

        print("Getting " + request.url + " from selenium")

        self.driver.get(unquote_plus(
            request.url))  # Decode url otherwise firefox is not happy. Ex /#%21/ => /#!/%21
        time.sleep(spider.js_wait)
        body = self.driver.page_source.encode('utf-8')
        url = self.driver.current_url

        return HtmlResponse(
            url=url,
            body=body,
            encoding='utf8'
        )

    def process_response(self, request, response, spider):
        # Since scrappy use start_urls and stop_urls before creating the request
        # If the url get redirected then this url gets crawled even if it's not allowed to
        # So we check if the final url is allowed

        if spider.remove_get_params:
            o = urlparse(response.url)
            url_without_params = o.scheme + "://" + o.netloc + o.path
            response = response.replace(url=url_without_params)

        if response.url == request.url + '#':
            response = response.replace(url=request.url)

        return response
