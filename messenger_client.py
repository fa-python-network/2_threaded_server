import socket, threading, sys

def read():
    while True :
        data = sock.recv(1024)
        print(data.decode('utf-8'))
num_sock = int(input("Enter the socket number: "))
server = ('', num_sock)  
name = str(raw_input("Enter your name: ")) 
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('', 0))
sock.sendto(('\n'+name+' connect to server').encode('utf-8'), server)
thread = threading.Thread(target=read)
thread.start()
while True:
	print("", end="")
	messenge = str(raw_input())
	sock.sendto((name+': '+messenge).encode('utf-8'), server)