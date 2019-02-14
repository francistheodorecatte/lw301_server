# coding: utf-8
from unittest import TestCase

from lw301_server_app import protocol


class TestMqttTrigger(TestCase):

    def test_mqtt_send(self):
        pass
        # raw = b'mac=00001234abcd&id=c2&pv=0&lb=0&ac=0&reg=0001&lost=0000&baro=982&ptr=0&wfor=0&p=1'
        # body = protocol.parse_body(raw)
        # self.assertIsNone(body.channel)
        # self.assertIsNone(body.sensor_values)
        # self.assertEqual(body.global_values, {'pressure_hPa': 982})
