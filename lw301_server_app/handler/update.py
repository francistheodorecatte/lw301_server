# coding: utf-8

import lw301_server_app.handler
from lw301_server_app import protocol, state
import hashlib
import uuid

class UpdateHandler(lw301_server_app.handler.Base):

    def generate_uuid(self, mac, channel, ref):
        base = "".join([str(mac), str(channel), str(ref)])
        md5sum = hashlib.md5()
        md5sum.update(base.encode('utf-8'))
        return str(uuid.UUID(md5sum.hexdigest()))

    async def post(self):
        if self.request.body is not None and len(self.request.body) > 0:
            self.log.debug('Raw body: {!r}'.format(self.request.body))
            body = protocol.parse_body(self.request.body, self.log)
            if body is not None:
                await self.process_parsed_body(body)
        else:
            self.log.debug('Empty body')
        # TODO: emulate real server answer
        self.add_header('Content-Type', 'application/json')
        self.write('')

    async def process_parsed_body(self, body):
        app_state = self.application.settings['lw301_state']
        self.log.debug(str(body))

        values = []

        if body.global_values and 'pressure_hPa' in body.global_values:
            values.append(('lw301', state.LW301(mac=body.mac, channel='0', id=self.generate_uuid(body.mac, '0', 'lw301'),
                 hPa=body.global_values['pressure_hPa'], forecast=body.global_values['weather_forecast'])))

        if body.sensor_values and 'temperature_celsius' in body.sensor_values:
            values.append((
                'temperature',
                 state.Temperature(mac=body.mac, channel=body.channel, id=self.generate_uuid(body.mac, body.channel, 'thgr8xx'),
                                   celsius=body.sensor_values['temperature_celsius'])
            ))

        if body.sensor_values and 'humidity_relative' in body.sensor_values:
            values.append((
                'humidity',
                 state.Humidity(mac=body.mac, channel=body.channel, id=self.generate_uuid(body.mac, body.channel, 'thgr8xx'),
                                   relative=body.sensor_values['humidity_relative'])
            ))

        if body.sensor_values and 'wind_direction' in body.sensor_values:
            values.append((
                'wind',
                state.Wind(mac=body.mac, channel=body.channel, id=self.generate_uuid(body.mac, body.channel, 'wgr800'),
                                   direction=body.sensor_values['wind_direction'],
                                   gust=body.sensor_values['wind_gust'],
                                   average=body.sensor_values['wind_speed'])
            ))

        if body.sensor_values and 'rain_rate' in body.sensor_values:
            values.append((
                'rain',
                state.Rain(mac=body.mac, channel=body.channel, id=self.generate_uuid(body.mac, body.channel, 'pcr800'),
                                   rate=body.sensor_values['rain_rate'],
                                   total=body.sensor_values['rain_total'])
            ))

        if body.sensor_values and 'uv_index' in body.sensor_values:
            values.append((
		'uv',
                state.UV(mac=body.mac, channel=body.channel, id=self.generate_uuid(body.mac, body.channel, 'uvn800'),
                                   index=body.sensor_values['uv_index'])
            ))

        for measurement, value in values:
            app_state.update_history(measurement, value)

        for trigger in self.application.settings['triggers']:
            for measurement, value in values:
                await trigger.on_new_data(measurement, value)
