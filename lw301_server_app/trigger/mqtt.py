# coding: utf-8
from logging import getLogger
import time
import json

from tornado.ioloop import IOLoop
from tornado.options import define, OptionParser
from tornado.httpclient import HTTPRequest, HTTPClientError

import paho.mqtt.client as mqtt

from lw301_server_app.trigger import Trigger


class MqttTrigger(Trigger):

    _as_tags = ('mac', 'channel')

    log = getLogger('mqtt_trigger')


    @staticmethod
    def add_options():
        define('mqtt-host', type=str)
        define('mqtt-port', type=int, default=1883)
        define('mqtt-clientid', type=str, default='lw301')
        define('mqtt-user', type=str, default=None)
        define('mqtt-password', type=str, default=None)

    def __init__(self, ioloop: IOLoop, app_options: OptionParser):
        super().__init__(ioloop, app_options)
        # self.http_client = AsyncHTTPClient()
        self.client = mqtt.Client()

        if self.app_options.mqtt_user is not None:
            self.client.username_pw_set(
                self.app_options.mqtt_user,
                self.app_options.mqtt_password,
            )

        self.client.connect(
            self.app_options.mqtt_host,
            self.app_options.mqtt_port
        )
        self.client.loop_start()
        # test self.client.publish("lw301/1/2", 10.2)

    def before_stop(self):
        self.client.loop_stop()

    async def on_new_data(self, measurement, value):
        v = value._asdict()

        ch = "" if ('channel' not in v or v['channel'] is None) else "_{}".format(v['channel'])

        self.client.publish("lw301/{}/{}".format(v['mac'], measurement), json.dumps(v))
