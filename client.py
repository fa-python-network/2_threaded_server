import socket
host="127.0.0.1"
port=8080
client=socket.socket()
client.connect((host, port))
client.send("This is from client".encode())
while True:
	in_data = client.recv(1024)
	print("From server: ", in_data.decode())
	out_data = input()
	client.send(out_data.encode())
	if out_data=="buy":
		break
client.close()