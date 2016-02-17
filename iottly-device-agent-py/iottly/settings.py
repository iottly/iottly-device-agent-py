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
default_settings = {

    'REGISTRATION_HOST': 'iottlycore:8520',
    'REGISTRATION_SERVICE': '/project/56c48d3cc9e741000dbc35f5/deviceregistration',
    'XMPP_SERVER_HOST': 'xmppbroker',
    'XMPP_SERVER_PORT': 5222,
    'XMPP_SERVER_USER': '',
    'JID': '',
    'PASSWORD': '',
    'CHUNK_SIZE': 1024    
}


class Settings:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

settings = Settings(**default_settings)