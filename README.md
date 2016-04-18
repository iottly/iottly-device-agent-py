# License

Copyright 2015 Stefano Terna

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# iottly-device-agent-py
The *iottly-device-agent-py* repo hosts the python agent which is itended to run on devices to enable them to communicate with Iottly.

We are currently running it on Raspberry Pi, and plan to test it on UDOO and port it to WiPy (Micro Python).

The agent is also shipped as a Docker container so to simplify the development environment.

# Setup instructions

Please refer to [Iottly docker](https://github.com/iottly/iottly-docker) for prerequisites and full Iottly stack setup.

# Setup and start the device locally in a container:
- first you need to create a project in Iottly, with board type "Dev Docker Device"
  - see [iottly-console](https://github.com/iottly/iottly-console/blob/master/README.md#iottly-usage) for instructions on how to create a project
- after that, `cd iottly`
- `cd iottly-device-agent-py`
- `./start_device_unattended.sh /bin/bash`
- this will:
  - pull the required image from Docker Hub
  - build the device image as per Dockerfile
  - start a new container in interactive mode, for development convenience
- once into the device container console:
  - copy/paste the agent install command from the previously created project (devices panel) 
  - launch the command which will:
    - download the agent installer customized from your IoT project
    - check and install newly available firmware in `/var/iottly-agent/userpackageuploads`
    - register the device
    - connect the device to Iottly
- `Ctrl C` to stop the agent
- `./start.sh` to run it again

On the shell you should see `JID set to: [uuid]@xmppbroker.localdev.iottly.org` to confirm that the service is running properly, and it successfully connected to the Iottly xmpp broker within the development (local) network.

On the Iottly project page you should see:
- a new row indicating that the device is correctly registered and its parameters
  - on the devices panel 
- a green 'led' and the messages produced by the Loop
  - on the Console panel, after choosing the board

From the Console panel, you can try to send command to the board.

Opening a new shell and repeating the full procedure will start a new device registering it to the project.

## Flashing a new firmware into the Dev Docker Device
You can flash a new firmware from the Device Code panel in [iottly-console](https://github.com/iottly/iottly-console/blob/master/README.md#iottly-usage).

A part from the fact that the agent will stop after receiving a new firmware and you need to restart it manually (with `./start.sh`), the feature works as if it was a physical device.

In physical devices the agent run as a service, with respawn, so it will automatically restart as soon as it is stopped.


# Setup and start the device on a Raspberry Pi:

### raspbian jessie LITE
The following instructions have been tested on the [raspbian jessie LITE](https://downloads.raspberrypi.org/raspbian_lite_latest):   
  - to flash image onto RPi SD card: [sd-and-micro-sd-management-with-linux-dd](http://tomorrowdata.io/2015/10/24/sd-and-micro-sd-management-with-linux-dd/)

### ssh into RPi (default user and password):
  - to find your RPi's IP: `sudo arp-scan [your local network]`
  - `[your local network]` can be for example: `192.168.1.0/24`
  - `ssh pi@[your RPi's IP]`

### once into the RPi console:
  - copy/paste the agent install command from the previously created project (devices panel in Iottly) 
  - launch the command which will:
    - download the agent installer customized from your IoT project
    - check and install newly available firmware in `/var/iottly-agent/userpackageuploads`
    - register the device
    - connect the device to Iottly

### to look at service logs: 
  - `sudo systemctl status iottly-device-agent.service`
