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

We are currently running it on Raspberry Pi, and plan to test it on UDOO and WiPy.

The agent is also shipped as a Docker container so to simplify the development environment.

# Setup instructions

Please refer to [Iottly docker](https://github.com/iottly/iottly-docker) for prerequisites and full Iottly stack setup.

# Setup and start the device locally in a container:

- `cd iottly`
- `cd iottly-device-agent-py`
- `./start_device.sh`
- this will:
  - pull the required image from Docker Hub
  - build the device image as per Dockerfile
  - start a new container in interactive mode, for development convenience
- once into the device container console:
  - `./start.sh` will run the device service

You should see `JID set to: raspdev.0001@xmppbroker.localdev.iottly.org` to confirm that the service is running properly.

# Setup and start the device on a Raspberry Pi:

### raspbian jessie LITE
The following instructions have been tested on the [raspbian jessie LITE](https://downloads.raspberrypi.org/raspbian_lite_latest):   
  - to flash image onto RPi SD card: [sd-and-micro-sd-management-with-linux-dd](http://tomorrowdata.io/2015/10/24/sd-and-micro-sd-management-with-linux-dd/)

### ssh into RPi (default user and password):
  - to find your RPi's IP: `sudo arp-scan 192.168.1.0/24` (if you are on a small network ...)
  - `ssh pi@[your RPi's IP]

### install python3.4
  - `sudo apt-get install python3.4`

### install pip:
  - `wget https://bootstrap.pypa.io/get-pip.py`
  - `sudo python3.4 get-pip.py`

### install python-dev (for GPIO build purposes)
  - `sudo apt-get install python3.4-dev`

### install RPi.GPIO:
  - this is just in case you want to have fun playing with GPIOs from the internet!
  - `sudo pip3.4 install RPi.GPIO`


### install git
  - `sudo apt-get install git`

### clone iottly-device-agent-py repo:
  - `git clone https://github.com/iottly/iottly-device-agent-py.git`
  - `cd iottly-device-agent-py`

### install iottly requirements:
  - `sudo pip3.4 install -r iottly-device-agent-py/requirements.txt`

### install service:
  - `./install-service.sh`

### run service:
  - `sudo systemctl start iottly-device-agent.service`
  - to see service logs: `sudo systemctl status iottly-device-agent.service`



# Configuration
The device is preconfigured with development parameters:
- [`settings.py`](https://github.com/iottly/iottly-device-agent-py/blob/master/iottly-device-agent-py/iottly/settings.py)

It tries to connect to the Iottly xmpp broker within the development (local) network.

If you have already started the full stack you should see the green 'led' onto the iottly-console panel.