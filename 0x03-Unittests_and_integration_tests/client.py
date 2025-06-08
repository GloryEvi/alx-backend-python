#!/usr/bin/env python3
"""
This module provides a client for interacting with GitHub organization data
through the GitHub API.
"""

from typing import Dict
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