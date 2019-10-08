import socket

ip = 'localhost'
port = 9100

sock = socket.socket()

sock.connect((ip,port))

sock.send("Hello from client!".encode())

data = sock.recv(1024)
print(data.decode())

sock.close()

