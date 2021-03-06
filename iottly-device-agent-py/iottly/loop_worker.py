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

import os, sys, time, logging
from multiprocessing import Process, Value
from ctypes import c_bool

class LoopWorker(Process):
    def __init__(self, loop_func, send_msg):
        Process.__init__(self, daemon=True)

        self.daemon = True

        self.name = loop_func.__name__

        self.loop_func = loop_func
        self.send_msg = send_msg

        # A shared flag to notify the thread that it should finish up and exit
        self.kill_received = Value(c_bool, False)

    def run(self):
        logging.info(' starting')
        self.send_msg({'process': {'name': self.name, 'status': 'started'}})

        while not self.kill_received.value:
            try:
                self.loop_func()
            except Exception as ex:
                #FIXME: add here debug message to be sent to iottly-core
                logging.error(ex)
                self.send_msg({
                    'process': 
                        {
                            'name': self.name, 
                            'function': self.name,
                            'status': {'error': '{}'.format(str(ex))},
                            'description': 'Oops this seems an error in your \'{}\' code'.format(self.name)
                        }
                    })                
                self.kill()

        logging.info(' exiting')


    def kill(self):
        logging.info("closing %s" % self.name)
        self.send_msg({'process': {'name': self.name, 'status': 'terminated'}})
        self.kill_received.value = True
        if self._parent_pid == os.getpid():
            self.terminate()
            self.join()
        logging.info("closed %s" % self.name)

