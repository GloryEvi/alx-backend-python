#!/usr/bin/env python3
"""
unit tests for the GithubOrgClient class
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
        
        # Verify the result matches the mock return value
        self.assertEqual(result, expected_org_data)
        
        # Verify get_json was called once with expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the expected list of repos.
        Mock get_json and _public_repos_url property.
        """
        # Define test payload - list of repositories from GitHub API
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
            {"name": "repo4", "license": {"key": "bsd-3-clause"}}
        ]
        
        # Expected result - just the repo names extracted from payload
        expected_repos = ["repo1", "repo2", "repo3", "repo4"]
        
        # Mock get_json to return our test payload
        mock_get_json.return_value = test_payload
        
        # Use patch as context manager to mock _public_repos_url property
        with patch.object(
            GithubOrgClient, 
            '_public_repos_url', 
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            
            # Set the return value for the mocked property
            test_repos_url = "https://api.github.com/orgs/test-org/repos"
            mock_public_repos_url.return_value = test_repos_url
            
            # Create client and call public_repos method
            client = GithubOrgClient("test-org")
            result = client.public_repos()
            
            # Test that the list of repos is what we expect from the chosen payload
            self.assertEqual(result, expected_repos)
            
            # Test that the mocked property was called once
            mock_public_repos_url.assert_called_once()
            
        # Test that the mocked get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(test_repos_url)


if __name__ == '__main__':
    unittest.main()