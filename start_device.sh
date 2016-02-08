docker build -t iottlyrpiagent .
docker run -it -v `pwd`/iottly-device-agent-py:/iottly-device-agent-py/iottly-device-agent-py --net iottlydocker_default iottlyrpiagent /bin/bash
