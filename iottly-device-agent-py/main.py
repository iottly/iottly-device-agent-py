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
                'status': {'error': '{}'.format(str(e))},
                'description': 'You may consider flashing a firmware.'
            }
        })


def checkfunction(funcname, notfoundaction, extramessagedata = None):
    if not udfw or (udfw and not hasattr(udfw, funcname)):
        msg = {'process': 
                    {
                        'name': current_process().name, 
                        'function': funcname,
                        'status': {'warning': 'Not Found'},
                        'description': 'No \'{}\' function found in userdefinedfw.'.format(funcname)
                    }}

        if extramessagedata:
            msg["process"].update(extramessagedata)

        notfoundaction(msg)

        return False
    else:
        return True


def main():

    loops = []

    # if any, add the loop function from the user package
    funcname = 'loop'
    if checkfunction(funcname, startupmessagelist.append):
        loops.append(getattr(udfw, funcname))

    #define the callback to receive messages from broker:
    def new_message(msg):
        #received message is a dictionary
        logging.info(msg)
        try:
            usermethodname = next(iter(msg.keys()))
            if len(msg.keys())<2:            
                if checkfunction(usermethodname, agent.send_msg, {'receivedcmd': msg}):
                    try:
                        getattr(udfw, usermethodname)(msg)
                    except Exception as e:
                        agent.send_msg({
                            'process': 
                                {
                                    'name': current_process().name, 
                                    'function': usermethodname,
                                    'status': {'error': '{}'.format(str(e))},
                                    'description': 'Oops this seems an error in your \'{}\' code'.format(usermethodname),
                                    'cmd': msg                                
                                }
                            })
            else:
                agent.send_msg({
                    'process': 
                        {
                            'name': current_process().name, 
                            'function': 'undefined',
                            'status': {'error': 'Too many methods defined'},
                            'description': 'Found JSON with more than 1 root key',
                            'cmd': msg                                
                        }
                    })

        except StopIteration as e:
            agent.send_msg({
                'process': 
                    {
                        'name': current_process().name, 
                        'function': 'undefined',
                        'status': {'error': '{}'.format(str(e))},
                        'description': 'No method name found in message',
                        'cmd': msg                                
                    }
                })

    #instantiate the agent passing:
    # - the message callback
    # - a list with the loop functions
    agent = rpi_agent.RPiIottlyAgent(new_message, loops)
    agentwrapper = iottlyagent.IottlyAgentWrapper(agent)

    #run init function, if any
    funcname = 'init'
    if checkfunction(funcname, startupmessagelist.append):
        try:
            getattr(udfw, funcname)()
        except Exception as e:
            startupmessagelist.append({
                'process': 
                    {
                        'name': current_process().name, 
                        'function': funcname,
                        'status': {'error': '{}'.format(str(e))},
                        'description': 'Oops this seems an error in your \'{}\' code'.format(funcname),
                    }
                })            


    # start the agent (blocking)
    agent.start(startupmessagelist)



if __name__ == '__main__':
    main()
