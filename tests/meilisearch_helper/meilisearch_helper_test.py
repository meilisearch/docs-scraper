# coding: utf-8
import json
from unittest.mock import patch

import requests

from scraper.src.config.version import __version__
from scraper.src.meilisearch_helper import MeiliSearchHelper
from tests.meilisearch_helper import common


class TestMeilisearchHelper:
    @patch("requests.delete")
    @patch("requests.patch")
    def test_use_meilisearch_default(self, mock_delete, mock_patch):
        mock_delete.configure_mock(__name__="delete")
        mock_response = requests.models.Response()
        mock_response.status_code = common.DEFAULT_ACCEPTED_STATUS
        mock_response._content = json.dumps(common.DEFAULT_DATA_DELETE).encode('utf-8')
        mock_delete.return_value = mock_response

        mock_patch.configure_mock(__name__="patch")
        mock_response = requests.models.Response()
        mock_response.status_code = common.DEFAULT_ACCEPTED_STATUS
        mock_response._content = json.dumps(common.DEFAULT_DATA_DELETE).encode('utf-8')
        mock_patch.return_value = mock_response
        """ Should set the `User-Agent` doscraper by default """
        # When
        actual = MeiliSearchHelper(
                common.BASE_URL,
                common.MASTER_KEY,
                common.DEFAULT_INDEX,
                MeiliSearchHelper.SETTINGS
            )

        # Then
        split_version = actual.meilisearch_client.http.headers['User-Agent'].split(";")
        assert len(split_version) == 2
        assert split_version[0].startswith("Meilisearch Python (") is True
        assert split_version[1] == f"Meilisearch DocsScraper (v{__version__})"
