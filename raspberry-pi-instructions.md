# Setup and start the Iottly Agent on a Raspberry Pi

### raspbian jessie LITE
The agent have been tested on the [raspbian jessie LITE](https://downloads.raspberrypi.org/raspbian_lite_latest):   
  - to flash image onto RPi SD card: [sd-and-micro-sd-management-with-linux-dd](http://tomorrowdata.io/2015/10/24/sd-and-micro-sd-management-with-linux-dd/)

### power on the Raspberry Pi
### connect it to your local network
  - LAN, or
  - WiFi (instructions [here](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md))

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
