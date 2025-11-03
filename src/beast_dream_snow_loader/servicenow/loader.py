"""Data loading functions for ServiceNow CMDB."""

from beast_dream_snow_loader.models.servicenow import (
    ServiceNowEndpoint,
    ServiceNowGatewayCI,
    ServiceNowLocation,
    ServiceNowNetworkDeviceCI,
)
from beast_dream_snow_loader.servicenow.api_client import ServiceNowAPIClient

# Table name mappings (ServiceNow standard tables or custom)
TABLE_GATEWAY_CI = "cmdb_ci_network_gateway"  # Standard ServiceNow table
TABLE_LOCATION = "cmdb_location"  # Standard ServiceNow table
TABLE_NETWORK_DEVICE_CI = "cmdb_ci_network_gear"  # Standard ServiceNow table
TABLE_ENDPOINT = "cmdb_endpoint"  # Standard ServiceNow table (or custom)


def load_gateway_ci(client: ServiceNowAPIClient, gateway: ServiceNowGatewayCI) -> dict:
    """Load a gateway CI record into ServiceNow.

    Args:
        client: ServiceNow API client
        gateway: Gateway CI model instance

    Returns:
        Created record data from ServiceNow
    """
    data = gateway.model_dump(exclude_none=True)
    return client.create_record(TABLE_GATEWAY_CI, data)


def load_location(client: ServiceNowAPIClient, location: ServiceNowLocation) -> dict:
    """Load a location record into ServiceNow.

    Args:
        client: ServiceNow API client
        location: Location model instance

    Returns:
        Created record data from ServiceNow
    """
    data = location.model_dump(exclude_none=True)
    return client.create_record(TABLE_LOCATION, data)


def load_network_device_ci(
    client: ServiceNowAPIClient, device: ServiceNowNetworkDeviceCI
) -> dict:
    """Load a network device CI record into ServiceNow.

    Args:
        client: ServiceNow API client
        device: Network device CI model instance

    Returns:
        Created record data from ServiceNow
    """
    data = device.model_dump(exclude_none=True)
    return client.create_record(TABLE_NETWORK_DEVICE_CI, data)


def load_endpoint(client: ServiceNowAPIClient, endpoint: ServiceNowEndpoint) -> dict:
    """Load an endpoint record into ServiceNow.

    Args:
        client: ServiceNow API client
        endpoint: Endpoint model instance

    Returns:
        Created record data from ServiceNow
    """
    data = endpoint.model_dump(exclude_none=True)
    return client.create_record(TABLE_ENDPOINT, data)
