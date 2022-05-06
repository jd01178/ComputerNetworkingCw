#Server.py

# We will need the following module to generate randomized lost packets
import random
import sys
from socket import *
import time
import datetime
import pickle
import hashlib
from threading import Thread
from time import sleep



# Present object
class Present:
    def __init__(self,name):
        self.name = name

# Acknowledge object for sending 'Thank you' messages
class Acknowledgement:
    def __init__(self,name):
        self.name = 'Thank you'

# Receipt object
class Receipt:
    def __init__(self, name, receiptNum):
       self.name = name
       self.receiptNum = receiptNum


# Packets object (contains present in data field)
class Packet:
    def __init__(self, srcAddress, destAddress, seqNum, ackNum, timeToLive, length, checksum, receiptNum, data):
        self.srcAddress = srcAddress
        self.destAddress = destAddress
        self.seqNum = seqNum
        self.ackNum = ackNum
        self.length = length
        self.timeToLive = timeToLive
        self.checksum = checksum
        self.receiptNum = receiptNum
        self.data =data

# List of presnts that server will try to send to client
packetsToSend = []


# Example presents that client will send
iPhone = Present('iPhone')
packet1 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, iPhone)
packetsToSend.append(packet1)


Watch = Present('Watch')
packet2 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, Watch)
packetsToSend.append(packet2)


MacbookAir = Present('MacbookAir')
packet3 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, MacbookAir)
packetsToSend.append(packet3)




Christmas_day = datetime.datetime(2022, 12, 25)
Boxing_day = datetime.datetime(2022, 12, 26)

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))


while True:


    # This is for testing
    todays_date = datetime.datetime(2022, 12, 26)


    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    data, address = serverSocket.recvfrom(1024)

    data_variable = pickle.loads(data)


    # Server cannot hold any more than 10 presents
    if len(packetsToSend) < 10:
        print("Storing %s on server ..." % data_variable.data.name)
        # Store on server if space
        packetsToSend.append(data_variable)
    else:
        print("Dropping present. Buffer full.")



    for packet in packetsToSend:


        if todays_date == Christmas_day:
            print('Merry christmas')
            # If rand is less is than 4, we consider the packet lost and do not respond
            #if rand < 4:
                #print(str(packet.data.name)+" timing out")
                #continue
                # Otherwise, the server responds
                # Pickle the object and send it to the server
            data_string = pickle.dumps(packet)


            serverSocket.sendto(data_string, packet.destAddress)



        if todays_date == Boxing_day:
            print('disconnecting clients')
            serverSocket.shutdown(1)
            serverSocket.close()
