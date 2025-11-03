"""ServiceNow REST API client for CMDB operations."""

import os
from typing import Any

import requests  # type: ignore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ServiceNowAPIClient:
    """ServiceNow REST API client with authentication and basic operations.

    Supports multiple authentication methods (in order of preference):
    1. API key (Basic Auth with API key as password) - recommended for production
       - Use with service account user (named user, no UI login)
    2. OAuth 2.0 token (Bearer token) - optional, can tie to service account
    3. Basic Auth (username/password) - development/testing only

    Production Pattern: Named service account user with API key (no UI login).
    See docs/servicenow_constraints.md for assumptions.
    """

    def __init__(
        self,
        instance: str | None = None,
        username: str | None = None,
        password: str | None = None,
        api_key: str | None = None,
        oauth_token: str | None = None,
    ):
        """Initialize ServiceNow API client.

        Args:
            instance: ServiceNow instance URL (e.g., 'dev12345.service-now.com')
            username: ServiceNow username (for Basic Auth or API key)
            password: ServiceNow password (for Basic Auth, fallback only)
            api_key: ServiceNow API key (preferred, used as password in Basic Auth)
            oauth_token: OAuth 2.0 access token (most secure, Bearer token)

        Authentication Priority:
        1. API key (SERVICENOW_API_KEY + SERVICENOW_USERNAME) - Recommended for production
           - Use service account user (named user, no UI login)
        2. OAuth token (SERVICENOW_OAUTH_TOKEN env var) - Optional, Bearer token
        3. Username/password (SERVICENOW_USERNAME/SERVICENOW_PASSWORD) - Development/testing only

        Credentials are loaded from:
        1. Function arguments (highest priority)
        2. Environment variables
        3. 1Password CLI (if available) - TODO: implement
        """
        self.instance = instance or os.getenv("SERVICENOW_INSTANCE", "")

        if not self.instance:
            raise ValueError("ServiceNow instance URL is required")

        # Ensure instance URL is clean (no https:// prefix)
        self.instance = (
            self.instance.replace("https://", "").replace("http://", "").rstrip("/")
        )

        self.base_url = f"https://{self.instance}/api/now"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Authentication: Priority 1 - API Key (Recommended for production)
        # Use service account user (named user, no UI login) with API key
        api_key = api_key or os.getenv("SERVICENOW_API_KEY", "")
        username = username or os.getenv("SERVICENOW_USERNAME", "")
        if api_key and username:
            self.session.auth = (username, api_key)
            return

        # Authentication: Priority 2 - OAuth Token (Optional)
        oauth_token = oauth_token or os.getenv("SERVICENOW_OAUTH_TOKEN", "")
        if oauth_token:
            self.session.headers["Authorization"] = f"Bearer {oauth_token}"
            return

        # Authentication: Priority 3 - Basic Auth (username/password) - Development/testing only
        # NOT recommended for production - use service account with API key instead
        password = password or os.getenv("SERVICENOW_PASSWORD", "")
        if username and password:
            self.session.auth = (username, password)
            return

        # No valid authentication found
        raise ValueError(
            "ServiceNow authentication required. Recommended for production:\n"
            "  - API key: SERVICENOW_API_KEY + SERVICENOW_USERNAME env vars\n"
            "    (Use service account user - named user, no UI login)\n"
            "  - OAuth token: SERVICENOW_OAUTH_TOKEN env var (optional)\n"
            "  - Username/password: SERVICENOW_USERNAME + SERVICENOW_PASSWORD env vars\n"
            "    (Development/testing only - NOT recommended for production)"
        )

    def create_record(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        """Create a record in a ServiceNow table.

        Args:
            table: ServiceNow table name (e.g., 'cmdb_ci_network_gateway')
            data: Record data as dictionary

        Returns:
            Created record data from ServiceNow

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.base_url}/table/{table}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json().get("result", {})  # type: ignore

    def get_record(self, table: str, sys_id: str) -> dict[str, Any] | None:
        """Get a record from a ServiceNow table by sys_id.

        Args:
            table: ServiceNow table name
            sys_id: Record sys_id

        Returns:
            Record data or None if not found

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.base_url}/table/{table}/{sys_id}"
        response = self.session.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json().get("result", {})  # type: ignore

    def update_record(
        self, table: str, sys_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a record in a ServiceNow table.

        Args:
            table: ServiceNow table name
            sys_id: Record sys_id
            data: Updated record data

        Returns:
            Updated record data from ServiceNow

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.base_url}/table/{table}/{sys_id}"
        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json().get("result", {})  # type: ignore

    def query_records(
        self, table: str, query: str | None = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Query records from a ServiceNow table.

        Args:
            table: ServiceNow table name
            query: ServiceNow encoded query string (e.g., 'name=test')
            limit: Maximum number of records to return

        Returns:
            List of record data dictionaries

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.base_url}/table/{table}"
        params: dict[str, Any] = {"sysparm_limit": limit}
        if query:
            params["sysparm_query"] = query

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json().get("result", [])  # type: ignore
