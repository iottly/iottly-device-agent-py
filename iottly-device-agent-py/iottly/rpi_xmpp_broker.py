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


import sleekxmpp
import os,sys
import logging



class RpiIottlyXmppBroker(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, message_from_broker):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.message_from_broker = message_from_broker

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.handle_message)

        self.use_signals(signals=['SIGHUP', 'SIGTERM', 'SIGINT'])
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping

        # If you want to verify the SSL certificates offered by a server:
        # xmpp.ca_certs = "path/to/ca/cert"
        # self.ssl_version = ssl.PROTOCOL_SSLv3
        # self.ca_certs = None
        self['feature_mechanisms'].unencrypted_plain = True

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def send_msg(self, to, msg):
        logging.info("Sending message %s %s" % (to, msg))
        self.send_message(mto=to,
                          mbody=msg,
                          mtype='chat')

    def handle_message(self, msg):
        msg = {
            'from': msg['from'],
            'to': msg['to'],
            'msg': msg['body']
        }

        logging.info(msg)

        self.message_from_broker(msg)


