import socket, threading

def send(uname):
	while True:
		msg = input('\n > ')
		data = uname + ':' + " " + msg
		cl_sock.send(data.encode())

def recv():
	while True:
		data = cl_sock.recv(1024)
		print('\n > '+ str(data.decode()))

cl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
uname = input('Enter your name to enter the chat > ')
cl_sock.connect(('localhost', 9128))     
print('Connected Successful!')
cl_sock.send(uname.encode())
thread_send = threading.Thread(target = send,args=[uname])
thread_send.start()
thread_recv = threading.Thread(target = recv)
thread_recv.start()