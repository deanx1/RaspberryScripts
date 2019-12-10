#!/usr/bin/python

# File: bleServer.py
# Auth: P Srinivas Rao
# Desc: Bluetooth server application that uses RFCOMM sockets

import os
import sys
import time
import logging
import logging.config
import json # Uses JSON package
import cPickle as pickle # Serializing and de-serializing a Python object structure
from bluetooth import * # Python Bluetooth library

logger = logging.getLogger('bleServerLogger')

def startLogging(
    default_path='configLogger.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    # Setup logging configuration
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

class bleServer:
    def __init__(self, serverSocket=None, clientSocket=None):
        if serverSocket is None:
            logger.info("serverSocket is None")
            self.dataObj = None
            self.addr = None
            # self.serverSocket = 12
            # self.clientSocket = 11
            self.serverSocket = serverSocket
            self.clientSocket = clientSocket
            self.serviceName="BluetoothServices"
            self.jsonFile ="text.json"
            self.uuid = "4b0164aa-1820-444e-83d4-3c702cfec373"
        else:
            # self.serverSocket = 12
            # self.clientSocket = 11
            self.addr = None
            self.serverSocket = serverSocket
            self.clientSocket = clientSocket
            logger.info("serverSocket is not None")

    def getBluetoothServices(self):
        try:
            logger.info("Searching for  Bluetooth services ...")
            for reConnect in range(2, 8):
                # bleService = find_service( name = "PI", uuid = self.uuid, address = self.addr )
                bleService = find_service( uuid = self.uuid, address = self.addr )
                logger.info("ADRESS\t: %s", self.addr)
                logger.info("UUID\t: %s", self.uuid)
                if len(bleService) == 0:
                    logger.info("Re-connecting  Bluetooth services : %d attempt", reConnect)
                else:
                    logger.info("BREAK BREAK BREAK")
                    break
            # if not bleService: raise SystemExit(), KeyboardInterrupt()
            if not bleService:
                logger.info("Not bleService!")
                raise SystemExit(), None
            else:
                logger.info("JAJAJAJAJ")
                logger.info("Found  Bluetooth services ..")
                logger.info("Protocol\t: %s", bleService[0]['protocol'])
                logger.info("Name\t\t: %s", bleService[0]['name'])
                logger.info("Service-id\t: %s", bleService[0]['service-id'])
                logger.info("Profiles\t: %s", bleService[0]['profiles'])
                logger.info("Service-class\t: %s", bleService[0]['service-classes'])
                logger.info("Host\t\t: %s", bleService[0]['host'])
                logger.info("Provider\t: %s", bleService[0]['provider'])
                logger.info("Port\t\t: %s", bleService[0]['port'])
                logger.info("Description\t: %s", bleService[0]['description'])
                self.bleService = bleService
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Couldn't find the RaspberryPi Bluetooth service : Invalid uuid", exc_info=True)

    def getBluetoothSocket(self):
        try:
            self.clientSocket=BluetoothSocket( RFCOMM )
            logger.info("Bluetooth client socket successfully created for RFCOMM service  ...")
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to create the bluetooth client socket for RFCOMM service  ...  ", exc_info=True)

    def getBluetoothConnection(self):
        try:
            bleServiceInfo = self.bleService[0]
            logger.info("Connecting to \"%s\" on %s with port %s" % (bleServiceInfo['name'], bleServiceInfo['host'], bleServiceInfo['port']))
            self.clientSocket.connect((bleServiceInfo['host'], bleServiceInfo['port']))
            logger.info("Connected successfully to %s "% (bleServiceInfo['name']))
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            # logger.error("Failed to connect to \"%s\" on address %s with port %s" % (bleServiceInfo['name'], bleServiceInfo['host'], bleServiceInfo['port']), exc_info=True)
            logger.error("Failed to connect to BLAH BLAH")

    # def getBluetoothSocket(self):
    #     try:
    #         self.serverSocket=BluetoothSocket( RFCOMM )
    #         logger.info("Bluetooth server socket successfully created for RFCOMM service...")
    #     except (BluetoothError, SystemExit, KeyboardInterrupt) as e:
    #         logger.error("Failed to create the bluetooth server socket ", exc_info=True)

    # def getBluetoothConnection(self):
    #     try:
    #         self.serverSocket.bind(("",PORT_ANY))
    #         logger.info("Bluetooth server socket bind successfully on host "" to PORT_ANY...")
    #     except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
    #         logger.error("Failed to bind server socket on host to PORT_ANY ... ", exc_info=True)
    #     try:
    #         self.serverSocket.listen(1)
    #         logger.info("Bluetooth server socket put to listening mode successfully ...")
    #     except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
    #         logger.error("Failed to put server socket to listening mode  ... ", exc_info=True)
    #     try:
    #         port=self.serverSocket.getsockname()[1]
    #         logger.info("Waiting for connection on RFCOMM channel %d" % (port))
    #     except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
    #         logger.error("Failed to get connection on RFCOMM channel  ... ", exc_info=True)

    # def advertiseBluetoothService(self):
    #     try:
    #         advertise_service( self.serverSocket, self.serviceName,
    #                         service_id = self.uuid,
    #                         service_classes = [ self.uuid, SERIAL_PORT_CLASS ],
    #                         profiles = [ SERIAL_PORT_PROFILE ],
    #     #                   protocols = [ OBEX_UUID ]
    #                         )
    #         logger.info("%s advertised successfully ..." % (self.serviceName))
    #     except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
    #         logger.error("Failed to advertise bluetooth services  ... ", exc_info=True)

    # def acceptBluetoothConnection(self):
    #     try:
    #         self.clientSocket, clientInfo = self.serverSocket.accept()
    #         logger.info("Accepted bluetooth connection from %s", clientInfo)
    #     except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
    #         logger.error("Failed to accept bluetooth connection ... ", exc_info=True)

    def recvData(self):
        logger.info("recvData")
        try:
            while True:
                data= self.clientSocket.recv(1024)
                if not data:
                    print "ditsdsdte"
                    self.clientSocket.send("EmptyBufferResend")
                # remove the length bytes from the front of buffer
                # leave any remaining bytes in the buffer!
                # dataSizeStr, ignored, data = data.partition(':')
                # print "dsdfsdfitte" + dataSizeStr
                # dataSize = int(dataSizeStr)
                print "dit34435345te"
                if len(data) > 0:
                    print "ditte"
                    self.clientSocket.send("CorruptedBufferResend")
                else:
                    self.clientSocket.send("DataRecived")
                    print "Breaking"
                    break
                
                print "HIERO"
            logger.info("Data received successfully over bluetooth connection")
            print "returning"
            # print data
            return data
        except (Exception, IOError, BluetoothError) as e:
            pass

    def deserializedData(self, _dataRecv):
        print "deserialiez"
        # print _dataRecv
        # try:
        #     # self.dataObj=pickle.loads(_dataRecv)
        #     self.dataObj=json.load(_dataRecv)
        #     logger.info("Serialized string converted successfully to object")
        # except (Exception, pickle.UnpicklingError) as e:
        #     logger.error("Failed to de-serialized string ... ", exc_info=True)

    def writeJsonFile(self):
        try:
            # Open a file for writing
            jsonFileObj = open(self.jsonFile,"w")
            logger.info("%s file successfully opened to %s" % (self.jsonFile, jsonFileObj))
            # Save the dictionary into this file
            # (the 'indent=4' is optional, but makes it more readable)
            json.dump(self.dataObj,jsonFileObj, indent=4)
            logger.info("Content dumped successfully to the %s file" %(self.jsonFile))
            # Close the file
            jsonFileObj.close()
            logger.info("%s file successfully closed" %(self.jsonFile))
        except (Exception, IOError) as e:
            logger.error("Failed to write json contents to the file ... ", exc_info=True)

    def closeBluetoothSocket(self):
        try:
            self.clientSocket.close()
            self.serverSocket.close()
            logger.info("Bluetooth sockets successfully closed ...")
        except (Exception, BluetoothError) as e:
            logger.error("Failed to close the bluetooth sockets ", exc_info=True)

    def start(self):
        # Search for the RaspberryPi Bluetooth service
        self.getBluetoothServices()
        # Create the client socket
        self.getBluetoothSocket()
        # Connect to bluetooth service
        self.getBluetoothConnection()

    def receive(self):
            # receive data
            dataRecv=self.recvData()
            print "recieve33"
            # print dataRecv
            # de-serializing data
            # self.deserializedData(dataRecv)
            # Writing json object to the file
            # self.writeJsonFile()

    def stop(self):
            # Disconnecting bluetooth sockets
            self.closeBluetoothSocket()

if __name__ == '__main__':
    startLogging()
    bleSvr = bleServer()
    bleSvr.start()
    bleSvr.receive()
    bleSvr.stop()
