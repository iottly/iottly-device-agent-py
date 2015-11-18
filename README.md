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


# Setup instructions

Please refer to [Iottly docker](https://github.com/iottly/iottly-docker) for prerequisites and full Iottly stack setup.

# Setup and start the device

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

# Configuration
The device is preconfigured with development parameters:
- [`settings.py`](https://github.com/iottly/iottly-device-agent-py/blob/master/iottly-device-agent-py/iottly/settings.py)

It tries to connect to the Iottly xmpp broker within the development (local) network.

If you have already started the full stack you should see the green 'led' onto the iottly-console panel.