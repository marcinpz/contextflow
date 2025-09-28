# Jira API client

import requests
from typing import Dict, List, Any, Optional
import time


class JiraClient:
    """Client for Jira REST API."""

    def __init__(self, base_url: str, username: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.auth = (username, api_token)
        self.session = requests.Session()
        self.session.auth = self.auth

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request to Jira API."""
        url = f"{self.base_url}/rest/api/3/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_issues(self, jql: str = "", max_results: int = 50) -> List[Dict[str, Any]]:
        """Get issues matching JQL query."""
        params = {
            'jql': jql,
            'maxResults': max_results,
            'fields': 'key,summary,description,issuetype,status,assignee,reporter,created,updated,labels,priority,parent'
        }
        response = self._get('search', params)
        return response.get('issues', [])

    def get_epics(self, project_key: str) -> List[Dict[str, Any]]:
        """Get all epics in a project."""
        jql = f'project = {project_key} AND issuetype = Epic'
        return self.get_issues(jql)

    def get_stories_by_epic(self, epic_key: str) -> List[Dict[str, Any]]:
        """Get all stories linked to an epic."""
        jql = f'"Epic Link" = {epic_key}'
        return self.get_issues(jql)

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get single issue details."""
        return self._get(f'issue/{issue_key}')

    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects."""
        response = self._get('project')
        return response if isinstance(response, list) else []