#!/usr/bin/env python3
"""Tests for GithubOrgClient"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unittest for GithubOrgClient"""

    @parameterized.expand([("google"), ("abc")])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """Parameterize and patch org function"""
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"payload": True})
        mock_get_json.assert_called_once()
