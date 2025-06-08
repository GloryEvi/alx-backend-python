#!/usr/bin/env python3
"""
Unit tests for client module.

This module contains unit tests for the GithubOrgClient class
and its methods.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        # Set up mock return value
        expected_org_data = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_org_data
        
        # Create client instance and call org method
        client = GithubOrgClient(org_name)
        result = client.org()
        
        # Verify get_json was called once with expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        
        # Verify the result matches the mock return value
        self.assertEqual(result, expected_org_data)


if __name__ == '__main__':
    unittest.main()