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
- first you need to create a project in Iottly, with board type "Dev Docker Device"; go to [iottly-console](https://github.com/iottly/iottly-console) for instructions on how to create a project
- after that, `cd iottly`
- `cd iottly-device-agent-py`
- `./start_device.sh`
- this will:
  - pull the required image from Docker Hub
  - build the device image as per Dockerfile
  - start a new container in interactive mode, for development convenience
- once into the device container console:
  - copy/paste the agent install command from the previously created project (devices panel) 
  - launch the command which will:
    - download the agent customized installer from your IoT project
    - register the device
    - connect the device to Iottly
    - start an example Loop
- `Ctrl C` twice to stop the agent
- `./start.sh` to run it again

On the shell you should see `JID set to: [uuid]@xmppbroker.localdev.iottly.org` to confirm that the service is running properly, and it successfully connected to the Iottly xmpp broker within the development (local) network.

On the Iottly project page you should see:
- a new row indicating that the device is correctly registered and its parameters
  - on the devices panel 
- a green 'led' and the messages produced by the Loop
  - on the Console panel, after choosing the board

From the Console panel, you can try to send command to the board.

Opening a new shell and repeating the full procedure will start a new device registering it to the project.

# Setup and start the device on a Raspberry Pi:

The device installer for the Raspberry Pi is not released yet. So you will need to follow these steps manually.

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
  - `cd iottly-device-agent-py/iottly-device-agent-py` (yes, twice)

### install iottly requirements:
  - `sudo pip3.4 install -r requirements.txt`

### install service:
  - `./install-service.sh`

### run service:
  - `sudo systemctl start iottly-device-agent.service`
  - to see service logs: `sudo systemctl status iottly-device-agent.service`

