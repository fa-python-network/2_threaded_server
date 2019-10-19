import socket, threading
from tqdm import tqdm
def scanner(ip, port):
	nsock = socket.socket()
	try:
		conn = nsock.connect((ip,port))
		print("Port " +str(port)+ " is open")
		connect.close()
	except:
		pass

host = []

print("This is scanning program.")
while True:
	try:
		ip = raw_input('Enter the IP adress: ')
		hostt = ip.split(".")
		for i in hostt:
			try:
				if 0<=int(i)<=255:
					host.append(int(i))
				else:
					print("The IP adress is incorrect. Try again.")
					break
			except TypeError:
				print("The IP adress is incorrect. Try again.")
				break
		break
	except ValueError:
		print("The IP adress is incorrect. Try again.")


for i in tqdm(range(65536)):
	thread = threading.Thread(target=scanner, args=(ip,i))
	thread.start()