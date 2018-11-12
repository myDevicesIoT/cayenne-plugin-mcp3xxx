"""
This module provides classes for interfacing with MCP extensions.
"""
import os
import time

from myDevices.devices.analog.mcp3x0x import MCP3002, MCP3004, MCP3008, MCP3204, MCP3208
from myDevices.plugins.analog import AnalogInput


class MCPInput(AnalogInput):
    """Class for interacting with a MCP input channel"""

    def read(self, channel):
        """Gets the analog value for the channel as a tuple with the type."""
        return (self.read_float(channel), 'analog_sensor')
