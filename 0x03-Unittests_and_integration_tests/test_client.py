#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class
and its methods.
"""

import unittest
from unittest.mock import patch, PropertyMock
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

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL."""
        # Mock payload that org property should return
        mock_payload = {
            "login": "test-org",
            "id": 12345,
            "repos_url": "https://api.github.com/orgs/test-org/repos"
        }
        
        # Use patch as context manager to mock the org property
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_payload
            
            # Create client instance
            client = GithubOrgClient("test-org")
            
            # Test that _public_repos_url returns the expected repos_url
            expected_url = "https://api.github.com/orgs/test-org/repos"
            self.assertEqual(client._public_repos_url, expected_url)


if __name__ == '__main__':
    unittest.main()