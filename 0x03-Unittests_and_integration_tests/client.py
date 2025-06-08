#!/usr/bin/env python3
"""
client for interacting with GitHub organization data
through the GitHub API.
"""
from typing import Dict, List
from utils import get_json, memoize


class GithubOrgClient:
    """Client for GitHub organization data."""
    
    ORG_URL = "https://api.github.com/orgs/{org}"
    
    def __init__(self, org_name: str) -> None:
        """
        Initialize the GitHub organization client.
        
        Args:
            org_name: Name of the GitHub organization
        """
        self._org_name = org_name
    
    @memoize
    def org(self) -> Dict:
        """
        Get organization data from GitHub API.
        
        Returns:
            Dictionary containing organization information from GitHub API
        """
        url = self.ORG_URL.format(org=self._org_name)
        return get_json(url)
    
    @property
    def _public_repos_url(self) -> str:
        """
        Get the public repositories URL for the organization.
        
        Returns:
            URL string for accessing the organization's public repositories
        """
        return self.org["repos_url"]
    
    def public_repos(self) -> List[str]:
        """
        Get list of public repository names for the organization.
        
        Returns:
            List of repository names
        """
        repos_data = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos_data]
    
    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """
        Check if a repository has a specific license.
        
        Args:
            repo: Dictionary containing repository information
            license_key: License key to check for
            
        Returns:
            True if repository has the specified license, False otherwise
        """
        return repo.get("license", {}).get("key") == license_key