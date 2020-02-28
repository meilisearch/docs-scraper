import re
import copy

from urllib.parse import urlparse
from ..js_executor import JsExecutor


class UrlsParser:
    @staticmethod
    def parse(config_start_urls):
        start_urls = []
        for start_url in config_start_urls:
            if isinstance(start_url, str):
                start_url = {'url': start_url}

            start_url['compiled_url'] = re.compile(start_url['url'])

            if "scrape" not in start_url:
                start_url['scrape'] = True

            if "page_rank" not in start_url:
                start_url['page_rank'] = 0

            if "tags" not in start_url:
                start_url['tags'] = []

            if "selectors_key" not in start_url:
                start_url['selectors_key'] = 'default'

            matches = UrlsParser.get_url_variables_name(start_url['url'])

            start_url['url_attributes'] = {}
            for match in matches:
                if len(start_url['url']) > 2 and start_url['url'][-2:] == '?)':
                    print('\033[0;35mWARNING: ' + start_url[
                        'url'] + ' finish by a variable.'
                                 ' The regex probably won\'t work as expected.'
                                 ' Add a \'/\' or \'$\' to make it work properly\033[0m')
                start_url['url_attributes'][match] = None

            # If there is tag(s) we need to generate all possible urls
            if len(matches) > 0:
                values = {}
                for match in matches:
                    if 'variables' in start_url:
                        if match in start_url['variables']:
                            if isinstance(start_url['variables'][match], list):
                                values[match] = start_url['variables'][match]
                            else:
                                if 'url' in start_url['variables'][
                                    match] and 'js' in start_url['variables'][
                                    match]:
                                    executor = JsExecutor()
                                    values[match] = executor.execute(
                                        start_url['variables'][match]['url'],
                                        start_url['variables'][match]['js'])
                                else:
                                    raise Exception(
                                        "Bad arguments for variables." + match + " for url " +
                                        start_url['url'])
                        else:
                            raise Exception(
                                "Missing " + match + " in variables" + " for url " +
                                start_url['url'])

                start_urls = UrlsParser.geturls(start_url, matches[0],
                                                matches[1:], values,
                                                start_urls)

            # If there is no tag just keep it like this
            else:
                start_urls.append(start_url)

        return start_urls

    @staticmethod
    def get_url_variables_name(url):
        # Cache it to avoid to compile it several time
        if not hasattr(UrlsParser.get_url_variables_name, 'group_regex'):
            UrlsParser.get_url_variables_name.group_regex = re.compile(
                r'\(\?P<(.+?)>.+?\)')

        return re.findall(UrlsParser.get_url_variables_name.group_regex, url)

    @staticmethod
    def geturls(start_url, current_match, matches, values, start_urls):
        for value in values[current_match]:
            copy_start_url = copy.copy(start_url)
            copy_start_url['original_url'] = copy_start_url['url']
            copy_start_url['url'] = copy_start_url['url'].replace(
                "(?P<" + current_match + ">.*?)", value)
            copy_start_url['compiled_url'] = re.compile(copy_start_url['url'])
            # Fix reference issue
            copy_start_url['url_attributes'] = copy.deepcopy(
                start_url['url_attributes'])
            copy_start_url['url_attributes'][current_match] = value

            if len(matches) == 0:
                start_urls.append(copy_start_url)
            else:
                start_urls = UrlsParser.geturls(copy_start_url, matches[0],
                                                matches[1:], values,
                                                start_urls)

        return start_urls

    @staticmethod
    def get_extra_facets(start_urls):
        extra_facets = []
        for start_url in start_urls:
            for tag in start_url['url_attributes']:
                extra_facets.append(tag)

        extra_facets = set(extra_facets)

        return list(extra_facets)

    @staticmethod
    def build_allowed_domains(start_urls, stop_urls):
        def get_domain(url):
            """ Return domain name from url """
            return urlparse(url).netloc

        # Concatenating both list, being careful that they can be None
        all_urls = [_['url'] if not isinstance(_, str) else _ for _ in
                    start_urls] + stop_urls
        # Getting the list of domains for each of them
        all_domains = [get_domain(_) for _ in all_urls]
        # Removing duplicates
        all_domains_unique = []
        for domain in all_domains:
            if domain in all_domains_unique:
                continue
            all_domains_unique.append(domain)

        return all_domains_unique

    # Check if tags are defined for the current_page or one of the parent page
    @staticmethod
    def get_tags(current_page_url, start_urls):
        if current_page_url is not None:
            for start_url in start_urls:
                if start_url['compiled_url'].match(current_page_url):
                    return start_url['tags']
        return []

    # Check if a page_rank is defined for the current_page or one of the parent page
    @staticmethod
    def get_page_rank(current_page_url, start_urls):
        if current_page_url is not None:
            for start_url in start_urls:
                if start_url['compiled_url'].match(current_page_url):
                    return int(start_url['page_rank'])
        return 0

    @staticmethod
    def get_extra_attributes(current_page_url, start_urls):
        if current_page_url is not None:
            for start_url in start_urls:
                if start_url['compiled_url'].match(current_page_url):
                    if 'extra_attributes' in start_url:
                        return start_url['extra_attributes']
        return {}

    @staticmethod
    def get_url_variables(current_page_url, start_urls):
        for start_url in start_urls:
            compiled_url = start_url['compiled_url']
            result = re.search(compiled_url, current_page_url)

            if result:
                for attr in start_url['url_attributes']:
                    value = start_url['url_attributes'][attr]
                    if value is not None:
                        current_page_url = current_page_url.replace(value, '')
                        yield attr, value, current_page_url
