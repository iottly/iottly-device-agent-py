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

"""

Main module for IOTTLY AGENT for Raspberry Pi

Classes: 
  - RPiIottlyAgent: main base class for IOTTLY AGENT; 
                    provides communication and multi-threading 
                    enabling custom code of the user to communicate with IOTTLY


"""


import logging
import json
import threading
import signal

from iottly import loop_worker
from iottly import rpi_xmpp_broker as rxb
from iottly import settings
import multiprocessing


logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s [%(levelname)s] (%(processName)-9s) %(message)s',)


class RPiIottlyAgent(object):
    """

    Raspberry Pi IOTTLY Angent base class

    Method:
      __init__ 
      start
      send_msg
      close

    """

    def __init__(self, message_from_broker, loops = []):
        """
        constructor for RPiIottlyAgent
        message_from_broker: callback to which notify to client the incoming messages from broker
        loops: list of functions which will be run in one thread each inside and infinite loop
               to provide threading support to the user code

        """
        super(RPiIottlyAgent, self).__init__()

        self.broker_process = None

        self.message_from_broker = message_from_broker

        self.loops = loops

        self.loop_worker_processes = []

        self.msg_queue = multiprocessing.Queue()

        signal.signal(signal.SIGTERM, self.sig_handler)        
        signal.signal(signal.SIGINT, self.sig_handler)        
        signal.signal(signal.SIGSEGV, self.sig_handler)
        
    def sig_handler(self, _signo, _stack_frame):
        if _signo in [signal.SIGTERM, signal.SIGINT]:
            if multiprocessing.current_process().name == 'MainProcess':
                logging.info("closing")
                self.close()


    def handle_message(self, msg):
        logging.info(msg)
        msg_string = msg["msg"]
        if msg_string.startswith('/json'):
            # decode json message
            json_content = {}
            try:
                json_content = json.loads(msg_string[6:])   
            except ValueError:
                logging.error("JSON parsing has failed for "+msg_string[6:])
            if self.message_from_broker:
                self.message_from_broker(json_content)

        else:
            logging.info("bad message: %s" % msg)

    def start(self):
        """

        starts the AGENT
        behaviour:
        the support threads for functions in loops list are started first in non-blocking mode
        xmpp communication is then started in blocking mode

        """
        

        #start loops thread
        for l in self.loops:
            lw = loop_worker.LoopWorker(loop_func=l)
            self.loop_worker_processes.append(lw)
            lw.start()


            
        self.broker_process = rxb.init(settings.XMPP_SERVER, settings.JID + '/IB', settings.PASSWORD, self.handle_message, self.msg_queue)

        self.broker_process.join()

        

    def send_msg(self, msg):
        """

        sends messages to the IOTTLY broker
        it is to be used by client code to send messages

        """
        self.msg_queue.put(dict(to=settings.XMPP_SERVER_USER,msg='/json ' + json.dumps(msg)))


    def close(self):
        """Closes eventually running threads serving the functions in the loops list"""

        for lw in self.loop_worker_processes:
            lw.kill()

        logging.info("Closing Agent")
        self.msg_queue.put(None)
        if self.broker_process:
            self.broker_process.join()
        logging.info("Agent closed")

    def restart(self):
        self.close()
        self.start()

