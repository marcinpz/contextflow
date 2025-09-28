# Jira data collector for Neo4j storage

from typing import List, Dict, Any
from .client import JiraClient
from .models import JiraIssue, JiraProject
from neo4j_integration.client import Neo4jClient


class JiraCollector:
    """Collects Jira data and stores it in Neo4j."""

    def __init__(self, jira_client: JiraClient, neo4j_client: Neo4jClient):
        self.jira_client = jira_client
        self.neo4j_client = neo4j_client

    def collect_project_epics_and_stories(self, project_key: str) -> Dict[str, Any]:
        """Collect all epics and their stories from a Jira project."""
        try:
            # Get all epics
            epics_data = self.jira_client.get_epics(project_key)
            epics = [self._parse_issue(epic) for epic in epics_data]

            # Get stories for each epic
            all_stories = []
            for epic in epics:
                stories_data = self.jira_client.get_stories_by_epic(epic.key)
                stories = [self._parse_issue(story) for story in stories_data]
                all_stories.extend(stories)

            # Store in Neo4j
            self._store_epics_and_stories(epics, all_stories)

            return {
                "project": project_key,
                "epics_collected": len(epics),
                "stories_collected": len(all_stories),
                "success": True
            }

        except Exception as e:
            return {
                "project": project_key,
                "error": str(e),
                "success": False
            }

    def _parse_issue(self, issue_data: Dict[str, Any]) -> JiraIssue:
        """Parse Jira API response into JiraIssue model."""
        fields = issue_data.get('fields', {})

        return JiraIssue(
            key=issue_data['key'],
            summary=fields.get('summary', ''),
            description=fields.get('description'),
            issue_type=fields.get('issuetype', {}).get('name', ''),
            status=fields.get('status', {}).get('name', ''),
            assignee=fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
            reporter=fields.get('reporter', {}).get('displayName', ''),
            created=fields.get('created', ''),
            updated=fields.get('updated', ''),
            labels=fields.get('labels', []),
            priority=fields.get('priority', {}).get('name') if fields.get('priority') else None,
            parent_key=fields.get('parent', {}).get('key') if fields.get('parent') else None
        )

    def _store_epics_and_stories(self, epics: List[JiraIssue], stories: List[JiraIssue]):
        """Store epics and stories in Neo4j with relationships."""
        # Create Epic nodes
        for epic in epics:
            query = """
            MERGE (e:Epic {key: $key})
            SET e.summary = $summary,
                e.description = $description,
                e.status = $status,
                e.assignee = $assignee,
                e.reporter = $reporter,
                e.created = $created,
                e.updated = $updated,
                e.labels = $labels,
                e.priority = $priority
            """
            self.neo4j_client.run_query(query, epic.model_dump())

        # Create Story nodes and relationships
        for story in stories:
            query = """
            MERGE (s:Story {key: $key})
            SET s.summary = $summary,
                s.description = $description,
                s.status = $status,
                s.assignee = $assignee,
                s.reporter = $reporter,
                s.created = $created,
                s.updated = $updated,
                s.labels = $labels,
                s.priority = $priority
            """
            self.neo4j_client.run_query(query, story.model_dump())

            # Create relationship to epic if parent_key exists
            if story.parent_key:
                query = """
                MATCH (s:Story {key: $story_key}), (e:Epic {key: $epic_key})
                MERGE (s)-[:BELONGS_TO]->(e)
                """
                self.neo4j_client.run_query(query, {
                    "story_key": story.key,
                    "epic_key": story.parent_key
                })