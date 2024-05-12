#!/usr/bin/env python3
"""Parameterize a unit test"""

import unittest
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
    def test_access_nested_map(self, nested_map, path, expected):
        """Base test cases"""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)
