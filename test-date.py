import datetime
import os
import json

#script to enbed in sensorscripts

dt = datetime.datetime.today()

# date = datetime.strptime(a, "%Y-%m-%d")
# print date

# Probleem = als de file te groot is kan deze wellicht niet verstuurd worden.
# Ergens moeten we data verwijderen

# Voordat we de data versturen maken we een backup genaamd data-backup. Je verstuurd het bestand.
# If successfully send: Slot 3 neemt data van slot 2, slot 2 neemt data van slot 1, de data-backup gaat in slot 1 
# 
# data file(file met nieuwe te versturen data) heet data.json


backup-slot-1
backup-slot-2
backup-slot-3

temperature = 8
humidity = 9

name = '/data_' + str(dt.year) + '_' + str(dt.month) + '.json'

currentDirectory = (os.path.dirname(os.path.realpath(__file__)))
print currentDirectory + name
# with open('/home/pi/Datamule/RaspberryScripts/BluetoothService/data_2019_12.json', 'a+') as outfile:
with open(currentDirectory + name, 'a+') as outfile:
    if os.stat(currentDirectory + name).st_size == 0:
        print "if"
        #if file not exist create object
        j = {}
        j["sensor"] = []
        j["sensor"].append({
            'temperature': temperature,
            'humidity': humidity,
            'datetime': str(dt.now())
        })
        json.dump(j, outfile)
    else:
        print "else"
        #if already exist add new sensor data
        j = json.load(outfile)
        outfile.truncate(0)
        j["sensor"].append({
              'temperature': temperature,
              'humidity': humidity,
              'datetime': str(dt.now())
        })
        json.dump(j, outfile)

    # else:
    #     print "else"



def createNewFile():
    print "newfile"

def checkMonth():
    # logger.info("Setting discoverable to on")
    cmd = 'sudo hciconfig hci0 piscan'
    subprocess.check_output(cmd, shell = True )  
