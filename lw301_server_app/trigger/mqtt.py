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

        self.client.publish("lw301/{}_{}/{}".format(v['mac'], v['channel'], measurement), json.dumps(v))

    #     # delay processing for next ioloop tick
    #     self.ioloop.add_callback(
    #         self._send_data,
    #         value=value,
    #         measurement=measurement,
    #         write_url=self.app_options.influxdb_writeurl,
    #         user=self.app_options.influxdb_user,
    #         password=self.app_options.influxdb_password,
    #     )
    #
    # def _value(self, value):
    #     if isinstance(value, int):
    #         return '{}i'.format(value)
    #     elif isinstance(value, float):
    #         return '{:0.2f}'.format(value)
    #     return '{}'.format(value)
    #
    # def _tag_value(self, value):
    #     if isinstance(value, int):
    #         value = str(value)
    #     return self._value(value)
