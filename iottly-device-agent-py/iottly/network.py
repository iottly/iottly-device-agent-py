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
import fcntl, socket, struct

def getHwAddr(ifname):
    #adapted from https://gist.github.com/zhenyi2697/6080400
    #to python 3.x
    b = bytearray()
    b.extend(map(ord, ifname[:15]))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', b))
    return ':'.join('{:02x}'.format(x) for x in info[18:24])
