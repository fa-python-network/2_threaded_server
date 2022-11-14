import socket
from time import sleep

with socket.socket() as sock:
  sock.setblocking(1)
  sock.connect(('10.38.165.12', 9090))

  #msg = input()
  msg = "Hi!"
  sock.send(msg.encode())

  data = sock.recv(1024)

print(data.decode())
