import socket
import threading


list_of_open_ports=[]

def scan_port(host, num_of_port):
	"""
	функция сканирования порта
	"""
	try:
		conn = sock.connect((host, num_of_port))
		print("the {} port is open".format(num_of_port))
		list_of_open_ports.append(num_of_port)
		conn.close()
	except:
		print("the {} port is not available".format(num_of_port))
		pass

sock = socket.socket()
host=input("Enter your host or IP, please.\nIt can be 'localhost', or press 'Enter',\nor just input as it is. (Ex: 10.0.2.15)")

threads=[]
for i in range(9090,9150):
	"""
	распараллеливание сканирования портов
	"""
	potoc = threading.Thread(target=scan_port, args=(host,i))
	threads.append(potoc)
	potoc.start()

for i in threads:
	i.join()


print("\nThere ports that are available")
print(list_of_open_ports)