""" """

import sys
import logging

assert sys.version_info >= (3, 0)

_LOGGER = logging.getLogger(__name__)

__version__ = '0.0.1'

TURNON = 1
TURNOFF = 2
BELL = 4
TOGGLE = 8
DIM = 16
LEARN = 32
UP = 128
DOWN = 256
STOP = 512
RGBW = 1024
THERMOSTAT = 2048

TEMPERATURE = 'temp'
HUMIDITY = 'humidity'
RAINRATE = 'rrate'
RAINTOTAL = 'rtot'
WINDDIRECTION = 'wdir'
WINDAVERAGE = 'wavg'
WINDGUST = 'wgust'
UV = 'uv'
POWER = 'watt'
LUMINANCE = 'lum'
DEW_POINT = 'dewp'
BAROMETRIC_PRESSURE = 'barpress'

BATTERY_LOW = 255
BATTERY_UNKNOWN = 254
BATTERY_OK = 253
