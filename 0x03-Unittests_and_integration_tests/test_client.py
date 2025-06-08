#!/usr/bin/env python3
"""
integration tests for the GithubOrgClient class
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
import fixtures


@parameterized_class([
    {
        "org_payload": fixtures.TEST_PAYLOAD[0][0],
        "repos_payload": fixtures.TEST_PAYLOAD[0][1], 
        "expected_repos": fixtures.TEST_PAYLOAD[0][2],
        "apache2_repos": fixtures.TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Tests the public_repos method with real implementation,
    only mocking external HTTP requests via requests.get.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up class method to start patching requests.get.
        """
        def side_effect(url: str):
            """
            Side effect function for requests.get mock.
            Returns appropriate fixture data based on URL.
            
            Args:
                url: The URL being requested
                
            Returns:
                Mock response object with json() method
            """
            # Create a mock response object
            mock_response = Mock()
            
            # Return org payload for organization API URLs
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            # Return repos payload for repositories API URLs  
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            # Default return for unexpected URLs
            else:
                mock_response.json.return_value = {}
            
            return mock_response
        
        # Start the patcher for requests.get
        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()
    
    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tear down class method to stop patching requests.get.
        Stops the patcher that was started in setUpClass.
        """
        cls.get_patcher.stop()
    
    def test_public_repos(self) -> None:
        """
        Test the public_repos method in integration.
        Verifies that the method returns the expected list of repositories
        when using the mocked requests.get responses.
        """
        # Create client instance  
        client = GithubOrgClient("google")
        
        # Call public_repos method
        result = client.public_repos()
        
        # Assert that the result matches expected repos from fixtures
        self.assertEqual(result, self.expected_repos)
    
    def test_public_repos_with_license(self) -> None:
        """
        Test the public_repos method with license filtering.
        Verifies that the method correctly filters repositories by license
        when a license parameter is provided.
        """
        # Create client instance
        client = GithubOrgClient("google")
        
        # Call public_repos method with apache-2.0 license filter
        result = client.public_repos(license="apache-2.0")
        
        # Assert that the result matches expected apache2 repos from fixtures
        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()