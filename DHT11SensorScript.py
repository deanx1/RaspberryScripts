#!/usr/bin/python2

# This script is for the sensor DHT11

import glob
import time
import Adafruit_DHT
from datetime import datetime
import json
import os

data = {}
data['sensor'] = [] 

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

humidity = round(humidity, 2)
temperature = round(temperature, 2)

if humidity is not None and temperature is not None:

  print 'Temperatuur: {0:0.1f}*C'.format(temperature)
  print 'Luchtvochtigheid: {0:0.1f}%'.format(humidity)
  print datetime.now()

  with open('/home/pi/Datamule/RaspberryScripts/BluetoothService/data.json', 'a+') as outfile:

        if os.stat('/home/pi/Datamule/RaspberryScripts/BluetoothService/data.json').st_size == 0:
          #if file not exist create object
          j = {}
          j["sensor"] = []
          j["sensor"].append({
            'temperature': temperature,
            'humidity': humidity,
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
  
#   data['sensor'].append({
#   'temperature': temperature,
#   'humidity': humidity,
#   'datetime': str(datetime.now())
# })

#   with open('/home/pi/Datamule/RaspberryScripts/BluetoothService/data.json', 'a+') as outfile:
#     json.dump(data, outfile)
  
else:
  print 'No data received'
