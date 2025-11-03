"""Unit tests for UniFi to ServiceNow transformation functions."""


from beast_dream_snow_loader.models.servicenow import ServiceNowGatewayCI
from beast_dream_snow_loader.models.unifi import UniFiHost
from beast_dream_snow_loader.transformers.unifi_to_snow import transform_host


class TestTransformHost:
    """Test transform_host function."""

    def test_transform_host_with_minimal_data(self):
        """Test transforming minimal UniFi host to ServiceNow gateway CI."""
        unifi_host = UniFiHost(
            id="test-host-id",
            hardwareId="UDM-Pro",
            type="gateway",
            ipAddress="192.168.1.1",
            owner=True,
            isBlocked=False,
            registrationTime="1700000000",
            lastConnectionStateChange="1700000000",
            latestBackupTime="1700000000",
            reportedState={
                "controller_uuid": "uuid-123",
                "host_type": 1,
                "hostname": "udm-pro",
                "mgmt_port": 8080,
                "name": "UDM-Pro",
                "state": "CONNECTED",
                "version": "1.12.33",
            },
            userData={"status": "ACTIVE"},
        )

        result = transform_host(unifi_host)

        assert isinstance(result, ServiceNowGatewayCI)
        assert result.sys_id == "test-host-id"
        assert result.hostname == "udm-pro"
        assert result.ip_address == "192.168.1.1"
        assert result.name == "UDM-Pro"
        assert result.firmware_version == "1.12.33"
        assert result.state == "CONNECTED"

    def test_transform_host_flattens_nested_fields(self):
        """Test that nested fields are properly flattened."""
        unifi_host = UniFiHost(
            id="test-host-id",
            hardwareId="UDM-Pro",
            type="gateway",
            ipAddress="192.168.1.1",
            owner=True,
            isBlocked=False,
            registrationTime="1700000000",
            lastConnectionStateChange="1700000000",
            latestBackupTime="1700000000",
            reportedState={
                "controller_uuid": "uuid-123",
                "host_type": 1,
                "hostname": "udm-pro",
                "mgmt_port": 8080,
                "name": "UDM-Pro",
                "state": "CONNECTED",
                "version": "1.12.33",
                "hardware": {"mac": "00:11:22:33:44:55", "serialno": "ABC123"},
            },
            userData={"status": "ACTIVE"},
        )

        result = transform_host(unifi_host)

        assert result.mac_address == "00:11:22:33:44:55"
        assert result.serial_number == "ABC123"

    def test_transform_host_handles_missing_fields(self):
        """Test that missing optional fields are handled gracefully."""
        unifi_host = UniFiHost(
            id="test-host-id",
            hardwareId="UDM-Pro",
            type="gateway",
            ipAddress="192.168.1.1",
            owner=True,
            isBlocked=False,
            registrationTime="1700000000",
            lastConnectionStateChange="1700000000",
            latestBackupTime="1700000000",
            reportedState={
                "controller_uuid": "uuid-123",
                "host_type": 1,
                "hostname": "udm-pro",
                "mgmt_port": 8080,
                "name": "UDM-Pro",
                "state": "CONNECTED",
                "version": "1.12.33",
            },
            userData={"status": "ACTIVE"},
        )

        result = transform_host(unifi_host)

        # Should not raise error, optional fields should be None
        assert result.mac_address is None or isinstance(result.mac_address, str)

    def test_transform_host_validates_output(self):
        """Test that output validates against ServiceNow model."""
        unifi_host = UniFiHost(
            id="test-host-id",
            hardwareId="UDM-Pro",
            type="gateway",
            ipAddress="192.168.1.1",
            owner=True,
            isBlocked=False,
            registrationTime="1700000000",
            lastConnectionStateChange="1700000000",
            latestBackupTime="1700000000",
            reportedState={
                "controller_uuid": "uuid-123",
                "host_type": 1,
                "hostname": "udm-pro",
                "mgmt_port": 8080,
                "name": "UDM-Pro",
                "state": "CONNECTED",
                "version": "1.12.33",
            },
            userData={"status": "ACTIVE"},
        )

        result = transform_host(unifi_host)

        # Should be valid ServiceNowGatewayCI instance
        assert isinstance(result, ServiceNowGatewayCI)
        # Should have required fields
        assert result.sys_id is not None
        assert result.name is not None
        assert result.ip_address is not None
        assert result.hostname is not None
