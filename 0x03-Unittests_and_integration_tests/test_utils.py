#!/usr/bin/env python3
"""Parameterize a unit test"""

from typing import Any, Dict, Mapping, Sequence
import unittest
from unittest.mock import Mock, patch
import utils
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Unittest for access_nested_map function"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Mapping, path: Sequence, expected: Any
    ) -> None:
        """Base test cases"""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(
        self, nested_map: Mapping, path: Sequence
    ) -> None:
        """Errors test cases"""
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Unittest for get_json function"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(
        self, test_utl: str, test_payload: Dict[str, bool], mock_get_json: Mock
    ):
        """Mock HTTP calls"""
        mock_get_json.return_value.json.return_value = test_payload
        self.assertEqual(utils.get_json(test_utl), test_payload)
        mock_get_json.assert_called_once_with(test_utl)
