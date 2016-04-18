# Setup and start a virtual device locally in a container
1. clone this repo: `git clone https://github.com/iottly/iottly-device-agent-py.git`
2. `cd iottly-device-agent-py`
3. `./start_device_unattended.sh /bin/bash`
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

On the shell you should see `JID set to: [uuid]@demobrober.iottly.org` to confirm that the service is running properly, and it successfully connected to the Iottly xmpp broker within the development (local) network.

On the Iottly project page you should see:
- a new row indicating that the device is correctly registered and its parameters
  - on the devices panel 
- a green 'led' and the messages produced by the Loop
  - on the Console panel, after choosing the board

Repeating the steps from 
From the Console panel, you can try to send command to the board.

Opening a new shell and repeating the full procedure will start a new device registering it to the project.

## Flashing a new firmware into the Dev Docker Device
You can flash a new firmware into the virtual device as it would be a physical one.

The only difference is that the agent will stop after receiving a new firmware and you need to restart it manually (with `./start.sh`).

In physical devices the agent run as a service, with respawn, so it will automatically restart as soon as it is stopped.

# Running other virtual devices
Repeat from step 3.
