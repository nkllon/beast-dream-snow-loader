"""ServiceNow CMDB data models using Pydantic for validation."""

from pydantic import BaseModel, ConfigDict, Field


class ServiceNowGatewayCI(BaseModel):
    """ServiceNow network gateway configuration item model."""

    model_config = ConfigDict(extra="allow")  # Allow additional fields from API

    sys_id: str = Field(..., description="Unique system identifier")
    name: str = Field(..., description="Gateway name")
    ip_address: str = Field(..., description="IP address")
    hostname: str = Field(..., description="Hostname")
    firmware_version: str | None = Field(None, description="Firmware version")
    hardware_id: str | None = Field(None, description="Hardware identifier")
    mac_address: str | None = Field(None, description="MAC address")
    serial_number: str | None = Field(None, description="Serial number")
    state: str | None = Field(None, description="Device state")


class ServiceNowLocation(BaseModel):
    """ServiceNow location/group record model."""

    model_config = ConfigDict(extra="allow")  # Allow additional fields from API

    sys_id: str = Field(..., description="Unique system identifier")
    name: str = Field(..., description="Location name")
    description: str = Field(..., description="Location description")
    timezone: str = Field(..., description="Timezone")
    host_id: str | None = Field(None, description="Foreign key to gateway")


class ServiceNowNetworkDeviceCI(BaseModel):
    """ServiceNow network device configuration item model."""

    model_config = ConfigDict(extra="allow")  # Allow additional fields from API

    sys_id: str = Field(..., description="Unique system identifier")
    name: str = Field(..., description="Device name")
    mac_address: str = Field(..., description="MAC address")
    serial_number: str | None = Field(None, description="Serial number")
    model: str | None = Field(None, description="Device model")
    site_id: str | None = Field(None, description="Foreign key to site")
    host_id: str | None = Field(None, description="Foreign key to host")


class ServiceNowEndpoint(BaseModel):
    """ServiceNow endpoint/client record model."""

    model_config = ConfigDict(extra="allow")  # Allow additional fields from API

    sys_id: str = Field(..., description="Unique system identifier")
    hostname: str = Field(..., description="Hostname")
    ip_address: str = Field(..., description="IP address")
    mac_address: str = Field(..., description="MAC address")
    device_type: str | None = Field(
        None, description="Device type (computer, phone, IoT, etc.)"
    )
    site_id: str | None = Field(None, description="Foreign key to site")
    device_id: str | None = Field(None, description="Foreign key to device")
