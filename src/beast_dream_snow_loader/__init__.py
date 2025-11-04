"""UniFi Dream Machine → ServiceNow CMDB Data Loader.

Load UniFi network infrastructure data into ServiceNow CMDB for network asset management.
"""

try:
    from ._version import __version__
except ImportError:
    # Fallback for development installs without hatch-vcs
    __version__ = "0.0.0+unknown"
