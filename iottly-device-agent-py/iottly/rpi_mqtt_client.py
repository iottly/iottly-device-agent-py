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

import paho.mqtt.client as mqtt

#import sleekxmpp
import os,sys
import time
import logging
from multiprocessing import Process, Queue

CONNECTED = 'Connected'
NOROUTETOHOST = 'NoRouteToHost'
PARAMERROR = 'ParamError'

class RpiIottlyMqttClient(mqtt.Client):
    def __init__(self,cl_id,pswd,message_from_broker,connection_status_changed):
        mqtt.Client.__init__(self,client_id=cl_id, clean_session=True, userdata=None)
        self.username_pw_set(cl_id, password=pswd)
        self.on_connect=connection_status_changed
        self.on_message=self.handle_message
        self.message_from_broker=message_from_broker
        self.verify_connection=connection_status_changed

    def handle_message (self, paho_mqtt, userdata, msg):
        print ("arriva")
        logging.info('New Message Received {}'.format("topic: "+str(msg.topic)+"\tpayload: "+str(msg.payload)))
        messg = {
            'topic': (str(msg.topic)),
            'msg': (str(msg.payload))
        }
        self.message_from_broker(messg)


# This function runs in its own process and dispatches messages in the shared queue
def message_consumer(mqtt_server, mqtt_port, mqtt_user, pswd, sub_tpc, pub_tpc, handle_message, msg_queue, child_conn):

    def connection_status_changed(client, userdata, flags, connection_status_code):
        logging.info('Connection to message broker STATUS - result code {}'.format(str(connection_status_code)))
        if (connection_status_code!=0):
            logging.info("no connection to %s" % str(mqtt_server))
            child_conn.send(NOROUTETOHOST)

    try:
        mqtt_c = RpiIottlyMqttClient(mqtt_user, pswd, handle_message, connection_status_changed)

        # Connect to the XMPP server and start processing XMPP stanzas.
        mqtt_c.connect(mqtt_server,mqtt_port,60)
        mqtt_c.subscribe(sub_tpc,2)
        mqtt_c.loop_start()
        child_conn.send(CONNECTED)

        while True:
            msg_obj = msg_queue.get()
            if msg_obj is None:
                logging.info("kill received")
                mqtt_c.unsubscribe(sub_tpc)
                mqtt_c.disconnect()
                break
            mqtt_c.publish(pub_tpc,msg_obj['msg'],2)

    except Exception as e:
        logging.info('msg_queue: {}'.format(msg_queue.qsize()))
        logging.exception(e)
        child_conn.send(PARAMERROR)


def init(mqtt_server, mqtt_port, mqtt_user, mqtt_password, sub_tpc, pub_tpc, handle_message, msg_queue, child_conn):
    # Interprocess queue for dispatching xmpp messages

    msg_process = Process(target=message_consumer, args=(mqtt_server, mqtt_port, mqtt_user, mqtt_password, sub_tpc, pub_tpc, handle_message, msg_queue, child_conn))
    msg_process.name = 'msg_process'
    msg_process.daemon = True
    msg_process.start()

    return msg_process