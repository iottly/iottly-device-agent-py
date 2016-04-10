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

import importlib
import time, datetime, os
import json
import logging
from multiprocessing import current_process

from iottly import iottlyagent
from iottly import rpi_agent



udfw = None
startupmessagelist = []
try:
    udfw = importlib.import_module('userpackage.userdefinedfw')
    fwdatetime = datetime.datetime.fromtimestamp(os.path.getmtime(udfw.__file__))
    logging.info('Found fw: {}'.format(fwdatetime))
    startupmessagelist.append({
        'process': 
            {
                'name': current_process().name, 
                'status': {'started': 'loaded firmware: {}'.format(fwdatetime)}
            }
        })
    
except Exception as e:
    logging.info(e)
    startupmessagelist.append({
        'process': 
            {
                'name': current_process().name, 
                'status': {'error': '{}. You may consider flashing a firmware.'.format(str(e))}
            }
        })

def main():

    loops = []

    # if any, add the loop function from the user package
    if udfw:
        if hasattr(udfw, 'loop'):
            loops.append(udfw.loop)
        else:
            startupmessagelist.append({
                'process': 
                    {
                        'name': current_process().name, 
                        'status': {'warning': 'No loop function found in userdefinedfw. Are you sure you don\'t want a loop function?'}
                    }
                })            

    #define the callback to receive messages from broker:
    def new_message(msg):
        #received message is a dictionary
        logging.info(msg)
        if udfw:
            usermethodname = next(iter(msg.keys()))
            if hasattr(udfw, usermethodname):
                try:
                    getattr(udfw, usermethodname)(msg)
                except Exception as e:
                    agent.send_msg({
                        'process': 
                            {
                                'name': current_process().name, 
                                'status': {'error': '{}. Oops this seems an error in your \'{}\' code'.format(str(e), usermethodname)}
                            }
                        })
            else:
                agent.send_msg({
                'process': 
                    {
                        'name': current_process().name, 
                        'status': {'warning': 'No handler found for cmd userdefinedfw. You may consider flashing your new firwmare.'},
                        'cmd': msg
                    }
                })




    #instantiate the agent passing:
    # - the message callback
    # - a list with the loop functions
    agent = rpi_agent.RPiIottlyAgent(new_message, loops)
    agentwrapper = iottlyagent.IottlyAgentWrapper(agent)

    # prepare startupmessages to be sent
    for msg in startupmessagelist:
        agent.send_msg(msg)

    # start the agent (blocking)
    agent.start()



if __name__ == '__main__':
    main()
