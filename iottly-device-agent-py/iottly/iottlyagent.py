
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