#!/usr/bin/python2

# This script is for the sensor DS18B20

import glob
import time
from datetime import datetime
import json
import os

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


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
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


def checkIfFileExists():
    currentDirectory = (os.path.dirname(os.path.realpath(__file__)))
    exists = os.path.isfile(currentDirectory + "/" + "BluetoothService/data.json")
    # exists = os.path.isfile('/home/pi/Datamule/RaspberryScripts/BluetoothService/data.json')
    print('checkIfFileExists:')
    print exists
    # return exists


temperature = read_temp()
temperature = round(temperature, 2)


if temperature is not None:

    print 'Temperatuur: {0:0.1f}*C'.format(temperature)
    print datetime.now()

    with open('/home/pi/Datamule/RaspberryScripts/BluetoothService/data.json', 'a+') as outfile:

        if os.stat('/home/pi/Datamule/RaspberryScripts/BluetoothService/data.json').st_size == 0:
          #if file not exist create object
          j = {}
          j["sensor"] = []
          j["sensor"].append({
            'temperature': temperature,
            'datetime': str(datetime.now())
          })
          json.dump(j, outfile)
        else:
          #if already exist add new sensor data
          j = json.load(outfile)
          outfile.truncate(0)
          j["sensor"].append({
              'temperature': temperature,
              'datetime': str(datetime.now())
          })
          json.dump(j, outfile)
else:
    print 'No data received'
