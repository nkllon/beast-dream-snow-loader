#!/usr/bin/env python3
"""Smoke test script for ServiceNow integration.

Usage:
    # Set environment variables
    export SERVICENOW_INSTANCE="dev12345.service-now.com"
    export SERVICENOW_USERNAME="admin"
    export SERVICENOW_PASSWORD="your-password"

    # Run smoke test
    python examples/smoke_test.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from beast_dream_snow_loader.models.servicenow import ServiceNowGatewayCI
from beast_dream_snow_loader.servicenow.api_client import ServiceNowAPIClient
from beast_dream_snow_loader.servicenow.loader import load_gateway_ci


def main():
    """Run smoke test: create a test gateway CI record in ServiceNow."""
    print("🚀 ServiceNow Smoke Test")
    print("=" * 50)

    try:
        # Initialize API client
        print("\n1. Initializing ServiceNow API client...")
        client = ServiceNowAPIClient()
        print(f"   ✓ Connected to instance: {client.instance}")

        # Create test gateway CI
        print("\n2. Creating test gateway CI record...")
        test_gateway = ServiceNowGatewayCI(
            u_unifi_source_id="smoke_test_gateway_001",  # Source ID, not sys_id
            name="Smoke Test Gateway",
            ip_address="192.168.1.1",
            hostname="smoke-test-gateway.example.com",
            firmware_version="1.0.0",
        )

        # Load into ServiceNow
        result = load_gateway_ci(client, test_gateway)
        print("   ✓ Record created successfully!")
        print(f"   ✓ sys_id: {result.get('sys_id', 'N/A')}")
        print(f"   ✓ name: {result.get('name', 'N/A')}")

        print("\n✅ Smoke test PASSED!")
        return 0

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease set environment variables:")
        print("  export SERVICENOW_INSTANCE='your-instance.service-now.com'")
        print("  export SERVICENOW_USERNAME='your-username'")
        print("  export SERVICENOW_PASSWORD='your-password'")
        return 1

    except Exception as e:
        print(f"\n❌ Smoke test FAILED: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
