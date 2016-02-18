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

import os
import json
import logging

class Settings:

    defaults = {

        'IOTTLY_REGISTRATION_HOST': '',
        'IOTTLY_REGISTRATION_SERVICE': '',
        'IOTTLY_XMPP_SERVER_HOST': '',
        'IOTTLY_XMPP_SERVER_PORT': 0,
        'IOTTLY_XMPP_SERVER_USER': '',
        'IOTTLY_XMPP_DEVICE_USER': '',
        'IOTTLY_XMPP_DEVICE_PASSWORD': '',
        'IOTTLY_CHUNK_SIZE': 1024    
    }



    def __init__(self, filename): 

        self.filename = filename
        #set defaults
        self.__dict__.update(self.defaults)


        #override from settings.json file
        try:
            with open(self.filename, 'r') as f:
                settings = json.loads(f.read())
                self.__dict__.update(settings)
        except:
            pass

        #override from env variables:
        self.__dict__.update({k: os.environ[k] for k in os.environ.keys() if k in self.defaults.keys()})

        logging.info(json.dumps({k: self.__dict__[k] for k in self.defaults.keys()},
                sort_keys=True, indent=4, separators=(',', ': ')))


    def save(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps({k: self.__dict__[k] for k in self.defaults.keys()},
                sort_keys=True, indent=4, separators=(',', ': ')))
