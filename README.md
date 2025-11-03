# beast-dream-snow-loader

**UniFi Dream Machine → ServiceNow CMDB Data Loader**

> Loading raw UniFi network infrastructure data into ServiceNow CMDB for network asset management and discovery.

## Overview

beast-dream-snow-loader transforms and loads UniFi network data (hosts, sites, devices, clients) from the UniFi API into ServiceNow CMDB tables. This enables ServiceNow to serve as the source of truth for network infrastructure.

**Purpose:** Complete the integration loop: UniFi API → Data Transformation → ServiceNow CMDB

## What It Does

1. **Reads UniFi Data:** Uses `beast_unifi` API clients to fetch raw UniFi data
2. **Transforms Data:** Maps UniFi schema to ServiceNow CMDB schema
3. **Creates ServiceNow Tables:** Defines and creates required CMDB tables
4. **Loads Data:** Syncs devices, sites, hosts, and clients to ServiceNow

## Project Status

🚧 **In Development** - Spec-driven development phase

## Source Data Schema

UniFi data structure (from `docs/unifi_schema.sql`):
- **hosts** - Gateway devices (Dream Machines, etc.)
- **sites** - UniFi sites/organizations
- **devices** - Network devices (switches, access points, etc.)
- **clients** - Network clients (computers, phones, TVs, thermostats, etc.)

## ServiceNow Integration

- **Target:** ServiceNow CMDB
- **Method:** REST API (via MID server for secure, authenticated access)
- **Tables:** ServiceNow CMDB tables for network infrastructure
- **Transformation:** UniFi schema → ServiceNow CMDB schema mapping

## Dependencies

- `beast-unifi-integration` - UniFi API clients
- ServiceNow REST API client
- ServiceNow MID server (for authentication)

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Project:** Part of the Beastmaster framework ecosystem  
**Repository:** `nkllon/beast-dream-snow-loader` (GitHub)

