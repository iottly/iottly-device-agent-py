"""

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

"""

class IottlyAgentWrapper:
    class __IottlyAgentWrapper:
        def __init__(self, agent):
            self.agent = agent
        def __str__(self):
            return repr(self) + self.agent
    instance = None
    def __init__(self, agent):
        if not IottlyAgentWrapper.instance:
            IottlyAgentWrapper.instance = IottlyAgentWrapper.__IottlyAgentWrapper(agent)
        else:
            IottlyAgentWrapper.instance.agent = agent
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def send_msg(self, msg):
        return self.agent.send_msg(msg)

agentwrapper = IottlyAgentWrapper(None)

send_msg = agentwrapper.send_msg