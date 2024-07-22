# coding: utf-8
import datetime
import collections

Temperature = collections.namedtuple('Temperature', ['mac', 'channel', 'celsius'])
Humidity = collections.namedtuple('Humidity', ['mac', 'channel', 'relative'])
Wind = collections.namedtuple('Wind', ['mac', 'channel', 'direction', 'gust', 'average'])
Rain = collections.namedtuple('Rain', ['mac', 'channel', 'rate', 'total'])
UV = collections.namedtuple('UV', ['mac', 'channel', 'index'])

class Pressure(collections.namedtuple('Pressure', ['mac', 'hPa'])):
    @property
    def mmHg(self):
        return int(self.hPa * 0.7500617)


class State:
    def __init__(self, history_limit=3000):
        self.temperature_history = []
        self.humidity_history = []
        self.pressure_history = []
        self.wind_history = []
        self.rain_history = []
        self.uv_history = []
        self.last_mac = None
        self._history_limit = history_limit

    def update_history(self, measurement, value):
        attr = '{}_history'.format(measurement)
        if not hasattr(self, attr) or type(getattr(self, attr)) != list:
            raise Exception('unknown measurement {}'.format(measurement))
        current_history = getattr(self, attr)
        if len(current_history) >= self._history_limit:
            current_history = current_history[-(self._history_limit-1):]
        self.last_mac = value.mac
        current_history.append((datetime.datetime.utcnow(), value))
        setattr(self, attr, current_history)
