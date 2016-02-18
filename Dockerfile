# 
# Copyright 2015 Stefano Terna
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

FROM ubuntu:latest
MAINTAINER iottly

RUN apt-get update -y

RUN apt-get install -y tar git curl nano wget
RUN apt-get install -y python3.4 python3-pip

RUN mkdir /iottly-device-agent-py
RUN mkdir /iottly-device-agent-py/iottly-device-agent-py

ADD requirements.txt /iottly-device-agent-py/requirements.txt
RUN python3.4 -m pip install -r /iottly-device-agent-py/requirements.txt

ENV TERM xterm

ADD /iottly-device-agent-py /iottly-device-agent-py/iottly-device-agent-py

WORKDIR /iottly-device-agent-py/iottly-device-agent-py

CMD ["python3.4", "main.py"] 