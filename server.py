import socket
from threading import Thread 

def accept_incoming_connections():
	""" Set up new clients """
	while True:
		client, client_address = server.accept()
		print("{} client has connected".format(client_address))
		client.send("Welcome everyone! Join the chat! Please, type your nickname so other chat users know, who sends messages".encode())
		addresses[client] = client_address
		Thread(target = handle_client, args=(client,)).start()

def handle_client(client):
	name = client.recv(1024).decode()
	welcome = "Welcome %s! If you want to quit, print {quit} to exit" %name
	client.send(welcome.encode())
	msg = "%s has joined the chat!" %name
	broadcast(msg.encode())
	clients[client] = name

	while True:
		msg = client.recv(1024)
		if msg!=bytes("{quit}", "utf8"):
			broadcast(msg, name+": ")
		else:
			client.send(bytes("{quit}", "utf8"))
			client.close()
			del clients[client]
			broadcast("{} has left the chat".format(name))
			break

def broadcast(msg, prefix=""):
	"""For all users"""
	for sock in clients:
		sock.send(bytes(prefix, "utf8")+msg)

clients={}
addresses={}

host="127.0.0.1"
port=7072

server=socket.socket()
server.bind((host, port))

if __name__ == "__main__":
	server.listen(2)
	print("Waiting connection...")
	accept_thread=Thread(target=accept_incoming_connections)
	accept_thread.start()
	accept_thread.join()
	server.close()
