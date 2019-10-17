
import socket
import random
from time import sleep
client = socket.socket()
client.setblocking(1)
client.connect(('localhost', 9095))
while True:
	data = input("Please, write the message: ")
	client.send(data.encode())
	if data=='bye':
		break
client.close()