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

import os, sys, threading, time, logging

class LoopWorker(threading.Thread):
    def __init__(self, loop_func):
        threading.Thread.__init__(self)

        self.name = loop_func.__name__

        self.loop_func = loop_func
        # A flag to notify the thread that it should finish up and exit
        self.kill_received = False

    def run(self):
        logging.info(' starting')
        while not self.kill_received:
            self.loop_func()
        logging.info(' exiting')


    def kill(self):
        self.kill_received = True
