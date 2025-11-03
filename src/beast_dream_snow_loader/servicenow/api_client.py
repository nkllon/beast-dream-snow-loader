"""ServiceNow REST API client for CMDB operations."""

import os
import shutil
import subprocess
from typing import Any

import requests  # type: ignore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _is_1password_available() -> bool:
    """Check if 1Password CLI is installed and available.

    Returns:
        True if 1Password CLI is installed, False otherwise
    """
    return shutil.which("op") is not None


def _is_1password_signed_in() -> bool:
    """Check if user is signed in to 1Password CLI.

    Returns:
        True if signed in, False otherwise (including if CLI not available)
    """
    if not _is_1password_available():
        return False

    try:
        result = subprocess.run(
            ["op", "account", "list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        # If command succeeds, user is signed in
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False


def _get_1password_credential(
    item_name: str, field: str, vault: str = "Beastmaster"
) -> str | None:
    """Get credential from 1Password CLI.

    Args:
        item_name: 1Password item name (e.g., "ServiceNow Dev Account")
        field: Field name (e.g., "username", "api_key", "password")
        vault: Vault name (default: "Beastmaster")

    Returns:
        Credential value as string, or None if not available or not signed in

    Note:
        Returns None if:
        - 1Password CLI not installed
        - User not signed in
        - Item/field not found
        - Command fails for any reason
    """
    if not _is_1password_signed_in():
        return None

    try:
        op_url = f"op://{vault}/{item_name}/{field}"
        result = subprocess.run(
            ["op", "read", op_url],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        return result.stdout.strip()
    except (
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
        FileNotFoundError,
    ):
        return None


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

        Credentials are loaded from (in priority order):
        1. Function arguments (highest priority)
        2. Environment variables
        3. 1Password CLI (if available AND signed in)
        """
        # Get instance URL (priority: arg → env → 1Password)
        if instance:
            self.instance = instance
        elif os.getenv("SERVICENOW_INSTANCE"):
            self.instance = os.getenv("SERVICENOW_INSTANCE", "")
        else:
            # Try 1Password (if available and signed in)
            op_instance = _get_1password_credential(
                "ServiceNow Dev Account", "instance"
            )
            self.instance = op_instance or ""

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
        # Try: function arg → env var → 1Password
        if api_key:
            api_key_value = api_key
        elif os.getenv("SERVICENOW_API_KEY"):
            api_key_value = os.getenv("SERVICENOW_API_KEY", "")
        else:
            api_key_value = (
                _get_1password_credential("ServiceNow Dev Account", "api_key") or ""
            )

        if username:
            username_value = username
        elif os.getenv("SERVICENOW_USERNAME"):
            username_value = os.getenv("SERVICENOW_USERNAME", "")
        else:
            username_value = (
                _get_1password_credential("ServiceNow Dev Account", "username") or ""
            )

        if api_key_value and username_value:
            self.session.auth = (username_value, api_key_value)
            return

        # Authentication: Priority 2 - OAuth Token (Optional)
        # Try: function arg → env var → 1Password
        if oauth_token:
            oauth_token_value = oauth_token
        elif os.getenv("SERVICENOW_OAUTH_TOKEN"):
            oauth_token_value = os.getenv("SERVICENOW_OAUTH_TOKEN", "")
        else:
            oauth_token_value = (
                _get_1password_credential("ServiceNow Dev Account", "oauth_token") or ""
            )

        if oauth_token_value:
            self.session.headers["Authorization"] = f"Bearer {oauth_token_value}"
            return

        # Authentication: Priority 3 - Basic Auth (username/password) - Development/testing only
        # NOT recommended for production - use service account with API key instead
        # Try: function arg → env var → 1Password
        if password:
            password_value = password
        elif os.getenv("SERVICENOW_PASSWORD"):
            password_value = os.getenv("SERVICENOW_PASSWORD", "")
        else:
            password_value = (
                _get_1password_credential("ServiceNow Dev Account", "password") or ""
            )

        if username_value and password_value:
            self.session.auth = (username_value, password_value)
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
