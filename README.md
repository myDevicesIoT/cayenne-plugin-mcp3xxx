# Cayenne MCP3XXX Plugin
A plugin allowing the [Cayenne Pi Agent](https://github.com/myDevicesIoT/Cayenne-Agent) to read data from MCP3XXX devices (MCP3002, MCP3004, MCP3008, MCP3204, MCP3208) and display it in the [Cayenne Dashboard](https://cayenne.mydevices.com).

## Requirements
### Hardware
* [Rasberry Pi](https://www.raspberrypi.org).
* An MCP3XXX extension, e.g. [MCP3008](https://www.adafruit.com/product/856).

### Software
* [Cayenne Pi Agent](https://github.com/myDevicesIoT/Cayenne-Agent). This can be installed from the [Cayenne Dashboard](https://cayenne.mydevices.com).
* [Git](https://git-scm.com/).

## Getting Started
1. Installation
   From the command line run the following commands to install this plugin.
   ```
   cd /etc/myDevices/plugins
   sudo git clone https://github.com/myDevicesIoT/cayenne-plugin-mcp3xxx.git
   ```

2. Setting the device class
   Specify the device you are using by setting the `class` value under the `MCP` section in the `cayenne-mcp3xxx.plugin` file.
   By default this is set to `MCP3008` but it can be set to use any of the classes in the `cayenne-mcp3xxx` module. If your 
   device has fewer channels than the `MCP3008` or you do not want the raw channel values to be displayed in the Cayenne 
   dashboard you can disable any of the individual input sections in `cayenne-mcp3xxx.plugin`.

3. Restarting the agent
   Restart the agent so it can load the plugin.
   ```
   sudo service myDevices restart
   ```