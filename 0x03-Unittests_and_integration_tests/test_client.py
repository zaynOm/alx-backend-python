#!/usr/bin/env python3
"""Tests for GithubOrgClient"""

import unittest
from unittest.mock import Mock, PropertyMock, patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unittest for GithubOrgClient"""

    @parameterized.expand(
        [
            ("google"),
            ("abc"),
        ]
    )
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """Parameterize and patch org function"""
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"payload": True})
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(url)

    def test_public_repos_url(self):
        """Mocking a property"""
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            payload = {"repos_url": "https://api.github.com/orgs/abc/repos"}
            mock_org.return_value = payload
            client = GithubOrgClient("abc")
            self.assertEqual(client._public_repos_url, payload["repos_url"])

    @patch(
        "client.get_json",
        return_value=[{"name": "repo1"}, {"name": "repo2"}],
    )
    def test_public_repos(self, mock_get_jdon: Mock) -> None:
        """More patching"""
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_pru:
            mock_pru.return_value = "https://api.github.com/orgs/abc/repos"
            client = GithubOrgClient("abc")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_jdon.assert_called_once()
            mock_pru.assert_called_once()
