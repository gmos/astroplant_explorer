"""
ae_drivers DS18B20 code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# This is a library module, nit intended to be called directly.
# See basic_demos/ds18b20_demo.py as a usage sample.

import time
import os
from . import _AE_Peripheral_Base

try:
    if os.system('sudo modprobe w1-gpio') or os.system('sudo modprobe w1-therm'):
        raise Exception('Abnormal DS18B20 system module load.')
except Exception as ex:
    print(ex, '\nDS18B20 and other 1-wire devices may not work!')

_W1_DIR = '/sys/bus/w1/devices/w1_bus_master1/'


class AE_DS18B20(_AE_Peripheral_Base):
    """Class to control a DS18B20 temperature sensor.
    Extendable for other devices.
    """

    def __init__(self, device_types=['28'], *arg, **kwarg):
        self._device_types = device_types

    def get_devices(self):
        with open(_W1_DIR + 'w1_master_slaves') as f:
            device_list = f.readlines()
        return sorted([dev_id.strip() for dev_id in device_list if dev_id[:2] in self._device_types])


device_file =  '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c



