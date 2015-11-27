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

import time
import json
import logging

from iottly import rpi_agent

def main():


    #define as many loop functions
    #loop functions are being runned in an infinite loop
    def loop1():
        logging.info('loop1')

        #msg is a dictionary (json):
        msg = {"timerevent": {"loop1message":1}}

        agent.send_msg(msg)
        time.sleep(1)

    def loop2():
        logging.info('loop2')

        #msg is a dictionary (json):
        msg = {"timerevent": {"loop1message":2}}

        agent.send_msg(msg)
        time.sleep(1)


    #define the callback to receive messages from broker:
    def new_message(msg):
        #received message is a dictionary
        logging.info(msg)
        agent.send_msg(msg)


    #instantiate the agent passing:
    # - the message callback
    # - a list with the loop functions
    agent = rpi_agent.RPiIottlyAgent(new_message, [loop1, loop2])

    agent.start()



if __name__ == '__main__':
    main()
