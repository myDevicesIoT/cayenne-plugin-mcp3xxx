"""
This module provides classes for interfacing with MCP3XXX extensions.
"""
import os
import time

from myDevices.devices.spi import SPI
from myDevices.devices.analog import ADC
from myDevices.plugins.analog import AnalogInput


class MCP3XXX(SPI, ADC):
    """Base class for interacting with MCP3XXX extensions."""

    def __init__(self, chip, vref, channel_count, resolution):
        """Initializes MCP3XXX device.

        Arguments:
        chip: The chip select
        vref: The reference voltage
        channel_count: Number of channels on the device
        resolution: Bits of resolution
        """
        self.channel_count = channel_count
        self.resolution = resolution
        SPI.__init__(self, chip, 0, 8, 10000)
        ADC.__init__(self, self.channel_count, self.resolution, float(vref))
        self.msb_mask = 2**(self.resolution - 8) - 1

    def __analogRead__(self, channel, diff=False):
        """Read the analog input. Overrides ADC.__analogRead__.

        channel: Channel on the device
        diff: True if using differential input
        """
        data = self._command(channel, diff)
        r = self.xfer(data)
        return ((r[1] & self.msb_mask) << 8) | r[2]

    def _command(self, channel, diff):
        """Format command data.

        channel: Channel on the device
        diff: True if using differential input
        """          
        d = [0x00, 0x00, 0x00]
        d[0] |= 1
        d[1] |= (not diff) << 7
        d[1] |= ((channel >> 2) & 0x01) << 6
        d[1] |= ((channel >> 1) & 0x01) << 5
        d[1] |= ((channel >> 0) & 0x01) << 4
        return d
        

class MCP3002(MCP3XXX):
    """Class for interacting with a MCP3002 device."""
    
    def __init__(self, chip=0, vref=3.3):
        """Initializes MCP3002 device.

        Arguments:
        chip: The chip select
        vref: The reference voltage
        """
        MCP3XXX.__init__(chip, vref, 2, 10)

    def __analogRead__(self, channel, diff=False):
        """Read the analog input. Overrides ADC.__analogRead__.

        channel: Channel on the device
        diff: True if using differential input
        """
        data = self._command(channel, diff)
        r = self.xfer(data)

        # Format of return is
        # 1 empty bit
        # 1 null bit
        # 10 ADC bits
        return (r[0]<<14 | r[1]<<6 | r[2]>>2) & ((2**self.resolution) - 1)

    def _command(self, channel, diff):
        """Format command data.

        channel: Channel on the device
        diff: True if using differential input
        """        
        d = [0x00, 0x00, 0x00]
        d[0] |= 1                 #start bit
        d[1] |= (not diff) << 7   #single/differential input
        d[1] |= channel << 6      #channel select
        return d


class MCP3004(MCP3XXX):
    """Class for interacting with a MCP3004 device."""
    
    def __init__(self, chip=0, vref=3.3):
        """Initializes MCP3004 device.

        Arguments:
        chip: The chip select
        vref: The reference voltage
        """
        MCP3XXX.__init__(chip, vref, 4, 10)


class MCP3008(MCP3XXX):
    """Class for interacting with a MCP3008 device."""
    
    def __init__(self, chip=0, vref=3.3):
        """Initializes MCP3008 device.

        Arguments:
        chip: The chip select
        vref: The reference voltage
        """
        MCP3XXX.__init__(self, chip, vref, 8, 10)


        
class MCP320X(MCP3XXX):
    """Class for interacting with MCP320X devices."""

    def __init__(self, chip, vref, channel_count):
        """Initializes MCP device.

        Arguments:
        chip: The chip select
        vref: The reference voltage
        channel_count: Number of channels on the device
        resolution: Bits of resolution
        """
        MCP3XXX.__init__(self, chip, vref, channel_count, 12)

    def _command(self, channel, diff):
        """Format command data.

        channel: Channel on the device
        diff: True if using differential input
        """
        d = [0x00, 0x00, 0x00]
        d[0] |= 1 << 2
        d[0] |= (not diff) << 1
        d[0] |= (channel >> 2) & 0x01
        d[1] |= ((channel >> 1) & 0x01) << 7
        d[1] |= ((channel >> 0) & 0x01) << 6
        return d


class MCP3204(MCP320X):
    """Class for interacting with a MCP3204 device."""

    def __init__(self, chip=0, vref=3.3):
        """Initializes MCP3204 device.

        Arguments:
        chip: The chip select
        vref: The reference voltage
        """
        MCP320X.__init__(self, chip, vref, 4)


class MCP3208(MCP320X):
    """Class for interacting with a MCP3208 device."""

    def __init__(self, chip=0, vref=3.3):
        """Initializes MCP3208 device.

        Arguments:
        chip: The chip select
        vref: The reference voltage
        """
        MCP320X.__init__(self, chip, vref, 8)


class MCPInput(AnalogInput):
    """Class for interacting with a MCP input channel."""

    def read(self, channel):
        """Gets the analog value for the channel as a tuple with the type."""
        return (self.read_float(channel), 'analog_sensor')
