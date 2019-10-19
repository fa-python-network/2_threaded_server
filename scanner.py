import socket
import threading


list_of_open_ports=[]

def scan_port(host, num_of_port):
	"""
	функция сканирования порта
	"""
	try:
		conn = sock.connect((host, num_of_port))
		#print("the {} port is open".format(num_of_port))
		list_of_open_ports.append(num_of_port)
		#conn.close()
	except:
		#print("the {} port is not available".format(num_of_port))
		pass

sock = socket.socket()
host=input("Enter your host or IP, please.\nIt can be 'localhost', or press 'Enter',\nItor just input as it is. (Ex: 10.0.2.15)")

print('\nwait...')			# почти как progress bar

threads=[]
for i in range(1,65536): 			
	"""
	распараллеливание сканирования портов
	"""
	potoc = threading.Thread(target=scan_port, args=(host,i))
	threads.append(potoc)
	potoc.start()

for i in threads:
	i.join()


print("\nAvailable ports are in the list below")
print(sorted(list_of_open_ports))