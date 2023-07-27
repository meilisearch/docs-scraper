# coding: utf-8
import re

from scraper.src.config.version import __version__


class TestInit:
    def test_get_version(self):
        assert re.match(r"^(\d+\.)?(\d+\.)?(\*|\d+)$", __version__)
