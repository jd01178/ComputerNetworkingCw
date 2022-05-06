# CC1.py

# We will need the following module to generate randomized lost packets
import random
import sys
import socket
import time
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
	def __init__(self, srcAddress, destAddress, seqNum, ackNum, length, timeToLive, checksum, receiptNum, data):
		self.srcAddress = srcAddress
		self.destAddress = destAddress
		self.seqNum = seqNum
		self.ackNum = ackNum
		self.length = length
		self.timeToLive = timeToLive
		self.checksum = checksum
		self.receiptNum = receiptNum
		self.data =data

		# Create a UDP socket
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12000

socket.setdefaulttimeout(1)
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientSock.bind(('', 12001))

# List of presnts that client will try to send to server
packetsToSend = []

# Example presents that client will send
shoe = Present('A new shoe')
packet1 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, shoe)
packetsToSend.append(packet1)


Ps5 = Present('Ps5')
packet2 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, Ps5)
packetsToSend.append(packet2)


Chocolate = Present('Chocolate')
packet3 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, Chocolate)
packetsToSend.append(packet3)


Television = Present('Television')
packet4 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, Television)
packetsToSend.append(packet4)


Sweater = Present('Sweater')
packet5 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, Sweater)
packetsToSend.append(packet5)


Airpods = Present('Airpods')
packet6 = Packet(('127.0.0.1', 12001), ('127.0.0.1', 12001),
1, 1, 8, 20, 0, 2, Airpods)
packetsToSend.append(packet6)


















# List of clients familyandfriendsList will try to send to server
familyandfriendsList = [('127.0.0.1', 12001)]






for packet in packetsToSend:
	# Send data
	#print ('sending "%s"' % Message)
	try:
		cur_time=time.time() *1000

		# Create an instance of ProcessData() to send to server.
		# Pickle the object and send it to the server
		data_string = pickle.dumps(packet)

		checksum = hashlib.md5(data_string).hexdigest()
		packet.checksum = checksum
		data_string = pickle.dumps(packet)

		print('Data Sent to Server')



		if packet.destAddress in familyandfriendsList:

			sent=clientSock.sendto(data_string, (UDP_IP_ADDRESS, UDP_PORT_NO))

		else:
			print('Attempting to send to non family/friend')


		# Receive response
		#print ('waiting to receive')
		data, server = clientSock.recvfrom(4096)

		data_variable = pickle.loads(data)

		receivedChecksum = data_variable.checksum

		data_variable.checksum = 0
		data_string = pickle.dumps(data_variable)
		calcChecksum = hashlib.md5(data_string).hexdigest()

		if data_variable.srcAddress in familyandfriendsList and receivedChecksum == calcChecksum:
			print ('Merry christmas! You received a(n) "%s" after "%2.3f" ms' % (data_variable.data.name, (time.time() *1000)-cur_time))


			ack =Acknowledgement()
			data_variable.data = ack
			data_variable.destAddress = data_variable.srcAddress
			data_variable.srcAddress = data_variable.destAddress
			data_string = pickle.dumps(data_variable)
			clientSock.sendto(data_string, data_variable.destAddress)



		elif data_variable.data.name == 'Thank you':
			packetsToSend.remove(packet)
			print('Present successfully delivered. Deleting present ...')
			continue

		elif receivedChecksum != calcChecksum:
			print ('checksum mismatch')









	except socket.timeout as inst:
		print('Request timed out')
print ('closing socket')
clientSock.close()
