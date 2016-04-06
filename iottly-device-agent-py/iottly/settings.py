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

import prettysettings

defaults = {

    'IOTTLY_PROJECT_ID': '',
    'IOTTLY_REGISTRATION_HOST': '',
    'IOTTLY_REGISTRATION_SERVICE': '',
    'IOTTLY_XMPP_SERVER_HOST': '',
    'IOTTLY_XMPP_SERVER_PORT': 0,
    'IOTTLY_XMPP_SERVER_USER': '',
    'IOTTLY_XMPP_DEVICE_USER': '',
    'IOTTLY_XMPP_DEVICE_PASSWORD': '',
    'IOTTLY_CHUNK_SIZE': 1024,
    'IOTTLY_SECRET_SALT': ''
}


def Settings():
    return prettysettings.Settings(defaults, './settings.json')

settings = Settings()