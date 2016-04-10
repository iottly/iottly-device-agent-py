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

import os
import logging
import json
import threading
import signal
import http.client
import multiprocessing

from iottly import network
from iottly import loop_worker
from iottly import rpi_xmpp_broker as rxb
from iottly.settings import settings
from iottly.flashmanager import FlashManager

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

        self.flashmanager = FlashManager(self.send_msg)

        self.child_conn, self.parent_conn = multiprocessing.Pipe()
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
            
            if json_content.get("fw"):
                self.flashmanager.handle_message(json_content)
            elif self.message_from_broker:
                self.message_from_broker(json_content)

        else:
            logging.info("bad message: %s" % msg)


    def connectionstatuschanged(self, status):
        if status == rxb.CONNECTED:
            #start loops thread
            for l in self.loops:
                lw = loop_worker.LoopWorker(loop_func=l, send_msg=self.send_msg)
                lw.start()            
        elif status == rxb.NOROUTETOHOST:
            self.close()
        elif status == rxb.PARAMERROR:
            logging.info('Ask for params to {}'.format(settings.IOTTLY_REGISTRATION_SERVICE))

            try:
                mac = network.getHwAddr('eth0')
                logging.info('device mac: {}'.format(mac))
                connection = http.client.HTTPConnection(settings.IOTTLY_REGISTRATION_HOST)

                reg_url = '{}/{}'.format(settings.IOTTLY_REGISTRATION_SERVICE, mac)
                logging.info(reg_url)
                connection.request('GET', reg_url)

                response = json.loads(connection.getresponse().read().decode())
                if 'error' in response.keys():
                    raise Exception(response['error'])

                settings.update(response)
                self.start()
            except Exception as e:
                logging.info(e)
                logging.info('Error retrieving params from IOTTLY')            
            

    def start(self):
        """

        starts the AGENT
        behaviour:
        the support threads for functions in loops list are started first in non-blocking mode
        xmpp communication is then started in blocking mode

        """

        #create uploadfirmware dir:
        if not os.path.exists(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR):
            os.makedirs(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR)

        try:
            self.broker_process = rxb.init(
                (settings.IOTTLY_XMPP_SERVER_HOST, settings.IOTTLY_XMPP_SERVER_PORT),
                settings.IOTTLY_XMPP_DEVICE_USER + '/IB', 
                settings.IOTTLY_XMPP_DEVICE_PASSWORD, 
                self.handle_message, 
                self.msg_queue, self.child_conn)

        except:
            self.child_conn.send(rxb.PARAMERROR)

        self.connectionstatuschanged(self.parent_conn.recv())

        if multiprocessing.current_process().name == 'MainProcess':
            # this is the blocking action on which the main process waits forever
            if self.parent_conn.recv() == "close":
                self._close()
        

    def send_msg(self, msg):
        """

        sends messages to the IOTTLY broker
        it is to be used by client code to send messages

        """
        self.msg_queue.put(dict(to=settings.IOTTLY_XMPP_SERVER_USER,msg='/json ' + json.dumps(msg)))


    def close(self):
        # close kills all the child processes
        # after having killed them it joins on each to wait for the child to really exit
        # in a multiprocess app child processes can't join other child process
        # only the parent process can join on its children
        # BUT if the close command is incoming from a broker message (a command from iottly)
        # then the execution process for the close is the msg_process which is itself a child
        # and hence not able to join on each of the other children

        # SO: the close command is enqueued to the parent process so that it can join 
        # the children

        self.child_conn.send("close")



    def _close(self):
        """Closes eventually running threads serving the functions in the loops list"""

        #to kill children loop over native children list
        #DO NOT create a custom process list
        #since terminated processes don't get correctly garbage collected
        for lw in multiprocessing.active_children():
            if type(lw) == loop_worker.LoopWorker:
                lw.kill()

        logging.info("Closing Agent")
        self.msg_queue.put(None)
        if self.broker_process:
            self.broker_process.join()
        logging.info("Agent closed")

    def restart(self):
        self.close()
        self.start()

