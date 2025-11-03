"""ServiceNow REST API client for CMDB operations."""

import os
from typing import Any

import requests  # type: ignore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ServiceNowAPIClient:
    """ServiceNow REST API client with authentication and basic operations."""

    def __init__(
        self,
        instance: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ):
        """Initialize ServiceNow API client.

        Args:
            instance: ServiceNow instance URL (e.g., 'dev12345.service-now.com')
            username: ServiceNow username
            password: ServiceNow password

        Credentials are loaded from:
        1. 1Password CLI (if available) - TODO: implement
        2. Environment variables (SERVICENOW_INSTANCE, SERVICENOW_USERNAME, SERVICENOW_PASSWORD)
        3. Function arguments (highest priority)
        """
        self.instance = instance or os.getenv("SERVICENOW_INSTANCE", "")
        self.username = username or os.getenv("SERVICENOW_USERNAME", "")
        self.password = password or os.getenv("SERVICENOW_PASSWORD", "")

        if not self.instance:
            raise ValueError("ServiceNow instance URL is required")
        if not self.username:
            raise ValueError("ServiceNow username is required")
        if not self.password:
            raise ValueError("ServiceNow password is required")

        # Ensure instance URL is clean (no https:// prefix)
        self.instance = (
            self.instance.replace("https://", "").replace("http://", "").rstrip("/")
        )

        self.base_url = f"https://{self.instance}/api/now"
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
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
