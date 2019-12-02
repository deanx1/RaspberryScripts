#!/usr/bin/python

# File: bleClient.py
# Auth: P Srinivas Rao
# Desc: Bluetooth client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
import os
import sys
import time
import logging
import logging.config
import json #Uses JSON package
import cPickle as pickle #Serializing and de-serializing a Python object structure
from datetime import datetime
from bluetooth import * #Python Bluetooth library
import subprocess
from threading import Thread

class EverySoOften(Thread):
    def __init__(self, seconds):
        '''Note that when you override __init__, you must 
           use super() to call __init__() in the base class
           so you'll get all the "chocolately-goodness" of
           threading (i.e., the magic that sets up the thread
           within the OS) or it won't work.
        '''        
        super(EverySoOften, self).__init__() 
        self.delay = seconds
        self.is_done = False
 
    def done(self):
        self.is_done = True
 
    def run(self):
        while not self.is_done:
            time.sleep(self.delay)
            setDiscoverable()
        print('thread done')

t = EverySoOften(60)
t.start()

logger = logging.getLogger('bleClientLogger')

def startLogging(
    default_path='configLogger.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    #Setup logging configuration
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# To make the pi always discoverable
def setDiscoverable():
    # logger.info("Setting discoverable to on")
    cmd = 'sudo hciconfig hci0 piscan'
    subprocess.check_output(cmd, shell = True )        

class bleClient:
    def __init__(self, serverSocket=None, clientSocket=None):

        # self.currentDirectory = os.getcwd()
        self.currentDirectory = (os.path.dirname(os.path.realpath(__file__)))
        logger.info("currentDirectory")
        logger.info(self.currentDirectory + "/" + "data.json")
        if serverSocket is None:
            logger.info("serverSocket is None1")
            # self.clientSocket = 11
            self.serverSocket = serverSocket
            self.clientSocket = clientSocket
            self.bleService = None
            self.addr = None
            self.uuid = "4b0164aa-1820-444e-83d4-3c702cfec373"
            self.serviceName="BluetoothServices"
            # self.jsonFile ="data.json"
            self.jsonFile =self.currentDirectory + "/" + "data-test.json"
            # self.jsonFile =self.currentDirectory + "/" + "data.json"
            # self.jsonFile ="data-test.json"
            self.jsonObj = None
        else:
            self.serverSocket = serverSocket
            self.clientSocket = clientSocket
            logger.info("serverSocket is not None2")

    def getBluetoothSocket(self):
        try:
            self.serverSocket=BluetoothSocket( RFCOMM )
            logger.info("Bluetooth server socket successfully created for RFCOMM service...")
        except (BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to create the bluetooth server socket ", exc_info=True)

    def getBluetoothConnection(self):
        try:
            self.serverSocket.bind(("",PORT_ANY))
            logger.info("Bluetooth server socket bind successfully on host "" to PORT_ANY...")
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to bind server socket on host to PORT_ANY ... ", exc_info=True)
        try:
            self.serverSocket.listen(1)
            logger.info("Bluetooth server socket put to listening mode successfully ...")
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to put server socket to listening mode  ... ", exc_info=True)
        try:
            port=self.serverSocket.getsockname()[1]
            logger.info("Waiting for connection on RFCOMM channel %d" % (port))
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to get connection on RFCOMM channel  ... ", exc_info=True)

    def advertiseBluetoothService(self):
        try:
            advertise_service( self.serverSocket, self.serviceName,
                            service_id = self.uuid,
                            service_classes = [ self.uuid, SERIAL_PORT_CLASS ],
                            profiles = [ SERIAL_PORT_PROFILE ],
        #                   protocols = [ OBEX_UUID ]
                            )
            logger.info("%s advertised successfully ..." % (self.serviceName))
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to advertise bluetooth services  ... ", exc_info=True)

    def acceptBluetoothConnection(self):
        try:
            self.clientSocket, clientInfo = self.serverSocket.accept()
            logger.info("Accepted bluetooth connection from %s", clientInfo)
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to accept bluetooth connection ... ", exc_info=True)

    def readJsonFile(self):
        try:
            jsonFileObj = open(self.jsonFile,"r")
            logger.info("File successfully uploaded to %s" % (jsonFileObj))
            self.jsonObj = json.load(jsonFileObj)
            logger.info("Content loaded successfully from the %s file" %(self.jsonFile))
            jsonFileObj.close()
        except (Exception, IOError) as e:
            logger.error("Failed to load content from the %s" % (self.jsonFile), exc_info=True)

    def serializeData(self):
        try:
            serializedData = json.dumps(self.jsonObj)
            logger.info("Object successfully converted to a serialized string")
            return serializedData
        except (Exception, pickle.PicklingError) as e:
            logger.error("Failed to convert json object  to serialized string", exc_info=True)

    def sendData(self, _serializedData):
        try:
            logger.info("Sending data over bluetooth connection")
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M ")
            # _serializedData = str(len(_serializedData))+ ":"+_serializedData
            _serializedData = dt_string +_serializedData
            self.clientSocket.send(_serializedData)
            time.sleep(0.5)
            logger.info("Sending data over bluetooth connection 2")
            while True:
                logger.info("Sending data over bluetooth connection 3")
                dataRecv = None
                try:
                    dataRecv= self.clientSocket.recv(1024)
                except:
                    logger.info("Android closed connection")
                logger.info("Sending data over bluetooth connection 4")

                if dataRecv in ['EmptyBufferResend', 'CorruptedBufferResend', 'DelimiterMissingBufferResend']:
                    logger.info("Sending data over bluetooth connection 5")
                    self.clientSocket.send(_serializedData)
                    logger.info("Sending data over bluetooth connection 6")
                    time.sleep(0.5)
                    logger.info("%s : Re-sending data over bluetooth connection" %(dataRecv))
                else:
                    break
            logger.info("Data sent successfully over bluetooth connection")
        except (Exception, IOError) as e:
            logger.error("Failed to send data over bluetooth connection", exc_info=True)

    def closeBluetoothSocket(self):
        try:
            self.clientSocket.close()
            logger.info("Bluetooth client socket successfully closed ...")
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to close the bluetooth client socket ", exc_info=True)

    # def start(self):
    #     # Search for the RaspberryPi Bluetooth service
    #     self.getBluetoothServices()
    #     # Create the client socket
    #     self.getBluetoothSocket()
    #     # Connect to bluetooth service
    #     self.getBluetoothConnection()

    def start(self):
            # Create the server socket
            self.getBluetoothSocket()
            # get bluetooth connection to port # of the first available
            self.getBluetoothConnection()
            # advertising bluetooth services
            self.advertiseBluetoothService()
            # Accepting bluetooth connection
            self.acceptBluetoothConnection()

    def send(self):
        # Socket send
        logger.info("Sending data over bluetooth connection")
    
        # self.clientSocket.send("Hello Daniel")
        # Load the contents from the file, which creates a new json object
        self.readJsonFile()
        # Convert the json object to a serialized string
        serializedData = self.serializeData()
        # Sending data over bluetooth connection
        self.sendData(serializedData)
        logger.info("send method done")


    def stop(self):
        # Disconnecting bluetooth service
        self.closeBluetoothSocket()
    
    def keepRunning(self):
        # Disconnecting bluetooth service
        while True:
            logger.info("Keep running in loop")
            bleClnt.start()
            bleClnt.send()
            

if __name__ == '__main__':
    setDiscoverable()
    startLogging()
    logger.info("Setup logging configuration")
    bleClnt = bleClient()
    bleClnt.start()
    bleClnt.send()
    bleClnt.stop()
    bleClnt.keepRunning()
