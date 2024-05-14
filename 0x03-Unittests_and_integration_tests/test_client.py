#!/usr/bin/env python3
"""Tests for GithubOrgClient"""

import unittest
from unittest.mock import Mock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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
        """Test public_repos function"""
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_pru:
            mock_pru.return_value = "https://api.github.com/orgs/abc/repos"
            client = GithubOrgClient("abc")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_jdon.assert_called_once()
            mock_pru.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected) -> None:
        """Test has_license function"""
        client = GithubOrgClient("abc")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(
    [
        {
            "org_payload": TEST_PAYLOAD[0][0],
            "repos_payload": TEST_PAYLOAD[0][1],
            "expected_repos": TEST_PAYLOAD[0][2],
            "apache2_repos": TEST_PAYLOAD[0][3],
        }
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """SetUpClass method"""

        def mock_requests_get(url):
            """Some side effects"""

            payloads = {
                "https://api.github.com/orgs/google": cls.org_payload,
                "https://api.github.com/orgs/google/repos": cls.repos_payload,
            }

            if url in payloads:
                return Mock(**{"json.return_value": payloads[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=mock_requests_get)
        cls.mock_get = cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        """TearDownClass method"""
        cls.patcher.stop()

    def test_public_repos(self):
        """Test public_repos"""
        github_org_client = GithubOrgClient("google")
        self.assertEqual(github_org_client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos apache-2.0 license"""
        github_org_client = GithubOrgClient("google")
        self.assertEqual(
            github_org_client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )
