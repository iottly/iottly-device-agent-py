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

BETA AGREEMENT

OurCompany has developed RASPBERRY IOTTLY AGENT including modifications, 
enhancements, improvements, updates, additions, derivative works, 
documentation and related material ("Software"). 
OurCompany desires that the Software be tested prior to general release.

Licensee agrees that Software is the sole property of OurCompany 
until it is officially released and includes valuable trade secrets of 
OurCompany. Licensee agrees to treat Software as confidential and 
will not without the express written authorization of OurCompany: 
- Demonstrate, copy, sell or market Software to any third party; 
- or Publish or otherwise disclose information relating to performance 
  or quality of the Software to any third party; 
- or Modify, reuse, disassemble, decompile, reverse engineer or otherwise 
  translate Software or any portion thereof. 

Software is provided "AS IS" without warranty of any kind. 
The entire risk arising out of the use or performance of Software remains 
with Licensee. In no event shall OurCompany be liable for any damage 
whatsoever arising out of the use of or inability to use Software, 
even if OurCompany has been advised of the possibility of such damages.

"""

__author__ = "Stefano Terna"
__copyright__ = "Copyright 2015, Stefano Terna"
__credits__ = []
__license__ = "BETA AGREEMENT"

__version__ = "0.6"
__maintainer__ = "Stefano Terna"
__email__ = "stefano.terna@tomorrowdata.io"
__status__ = "Prototype"


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
