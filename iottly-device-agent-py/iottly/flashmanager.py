import sleekxmpp
import os,sys
from iottly.ibcommands import Command
import logging
import base64
from hashlib import md5

from iottly.settings import settings

get_chunks = Command('Request chunks', 'Ask Iottly for some chunks', '/json {"fw":{"area":0,"block":0,"qty":0,"dim":0}}')

class FlashManager(object):
    def __init__(self, send_msg, close_func):
        self.chunks_received = 0
        self.last_block = -1
        self.chunks_desired = 4
        self.upgrade_area = 0
        self.md5 = None
        self.file = None
        self.projectid = None
        self.chunks = []
        self.send_msg = send_msg
        self.close_func = close_func

    def handle_message(self, msg):
        logging.info('flashmanager: {}'.format(str(msg)))
        if msg.get('fw'):
            fw = msg['fw']
            if fw.get('startupgrading') == 1:
                self.init_upgrade(msg)
            else:
                self.receive_chunk(msg)

    def _get_params(self):
        return {
            'fw.area': self.upgrade_area,
            'fw.block': self.last_block + 1,
            'fw.qty': self.chunks_desired,
            'fw.dim': int(settings.IOTTLY_CHUNK_SIZE/self.chunks_desired),
            'fw.file': self.file,
            'fw.projectid': settings.IOTTLY_PROJECT_ID
        }

    def init_upgrade(self, msg):
        self.upgrade_area = int(msg['fw'].get('area', -1))
        self.file = msg['fw'].get('file')
        self.projectid = msg['fw'].get('projectid')
        self.md5 = msg['fw'].get('md5')
        self.request_chunks(msg)
        self.chunks = []

    def request_chunks(self, msg):
        self.send_msg(get_chunks.to_json(**self._get_params()))
        self.chunks_received = 0

    def receive_chunk(self, msg):
        self.chunks_received += 1
        self.last_block = msg['fw'].get('block')
        data = msg['fw'].get('data')
        logging.info("Received chunk {}:[{}]".format(self.last_block, data))
        if data is None:
            logging.info("DONE!")
            self.last_block = -1
            self.dump_file()
            return
        else:
            self.chunks.append(data)

        if self.chunks_received == self.chunks_desired:
            self.request_chunks(msg)

    def dump_file(self):
        content = b''.join(map(base64.b64decode, self.chunks))
        real_content = content[:]
        logging.info('real_content: {}'.format(len(real_content)))

        while len(content) % settings.IOTTLY_CHUNK_SIZE:
            content += chr(0xFF)

        content += bytearray(settings.IOTTLY_SECRET_SALT,'utf-8')

        logging.info('Content length: {}'.format(len(content)))

        file_md5 = md5(content).hexdigest()
        logging.info("Expected MD5: {}".format(self.md5))
        logging.info("File MD5: {}".format(file_md5))
        if (file_md5 == self.md5):
            logging.info('md5 check passed! Save file.')
            
            with open(os.path.join(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR, self.file), 'wb') as f:
                f.write(real_content)

            logging.info('Closing agent to restart.')
            self.close_func()
