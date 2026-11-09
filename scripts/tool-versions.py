"""Offline model of the version comparison instructed in the agent and skills; no Hype calls."""
import re

EXPECTED_CATALOG_VERSION = 1
NOTICE = "Hype's tools changed. Run /mcp, then Reconnect, to pick them up."


def release(value):
    if not isinstance(value, str) or not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', value):
        raise ValueError('Version check unavailable')
    return tuple(map(int, value.split('.')))


def reconnect_notice(server_catalog, minimum_plugin, plugin_version):
    if type(server_catalog) is not int or server_catalog < 1:
        raise ValueError('Version check unavailable')
    minimum = release(minimum_plugin)
    installed = release(plugin_version)
    return NOTICE if server_catalog != EXPECTED_CATALOG_VERSION or minimum > installed else ''
