import socket
import threading, time

turned_off=False

def send_msg(conn: socket.socket,msg):
	"""
	отправка сообщений
	"""
	header=len(msg)
	formated_msg = f'{header:4}{msg}'.encode()
	conn.send(formated_msg)

def recv_msg(conn: socket.socket):
	"""
	принятие сообщений
	"""
	header=conn.recv(4).decode()
	msg=conn.recv(int(header))
	return msg.decode()


host=input("Enter your IP, please.\nInput 'localhost' or press 'Enter'.\nYou cal also input your IP as it is. (Example: 10.0.2.15)")
port=input("\nInput port that used by server: ")

sock = socket.socket()
sock.setblocking(1)

sock.connect((host,int(port)))

client_name=input("Enter your name: ")

tr=threading.Thread(target=recv_msg, args=(sock,))
tr.start()

joined=False

while turned_off==False:	
	if joined==False:
		send_msg(sock,f'{client_name} joined the chat')
		joined=True
	else:

		try:
			msg=input('You: ')

			if msg!='':
				send_msg(sock,msg)
			elif 'exit' in msg:
				raise Exception

			time.sleep(0.2)
		except:
			send_msg(sock, f'{client_name} left the chat')
			turned_off=True
tr.join()

sock.close()