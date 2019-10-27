from queue import Queue 
import socket
import threading
host = "127.0.0.1"
queue = Queue()
open_ports = []
def portscan(port):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))
		return True
	except:
		return False
def get_ports(count):
	for port in range(count):
		queue.put(port)
def worker():
	while not queue.empty():
		port=queue.get()
		if portscan(port):
			print("Port {} is openned!".format(port))
			open_ports.append(port)

import time
import sys

def run(threads, count):
	get_ports(count)
	thread_list=[]
	for i in range(threads):
		thread = threading.Thread(target=worker)
		thread_list.append(thread)
		time.sleep(0.001)
		sys.stdout.write("\r%d%%" % i)
		sys.stdout.flush()
	sys.stdout.write('\n')
	for thread in thread_list:
		thread.start()
	for thread in thread_list:
		thread.join()
	print("Open ports are: ", open_ports)
run(100, 1024)