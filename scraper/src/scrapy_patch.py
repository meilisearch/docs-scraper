from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory


# following https://github.com/scrapy/scrapy/issues/1429#issuecomment-131782133
# this seems to be the best option to avoid SSLv3 issues
class CustomContextFactory(ScrapyClientContextFactory):
    """
    Custom context factory that allows SSL negotiation.
    """

    def __init__(self):
        # Use SSLv23_METHOD so we can use protocol negotiation
        self.method = SSL.SSLv23_METHOD
