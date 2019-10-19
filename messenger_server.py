import socket, threading

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
num_sock = int(input("Enter the socket number: "))
f = 0
try:   
	sock.bind(('', num_sock))
except socket.error:
		print("This Adress already in use. This is free one: ")
		for i in range(1024,65536):
			try:
				sock.bind(('', i))
				f = i
				break
			except socket.error:
				pass

if f == 0:
	print(num_sock)
else:
	num_sock = f
	print(num_sock)

clients = [] 
while True :
         conn = sock.recvfrom(1024)
         data, addr = conn[0], conn[1]
         print (addr[0], addr[1])
         if  addr not in clients : 
                 clients.append(addr)
         for client in clients :
                 if client == addr : 
                     continue 
                 sock.sendto(data,client)