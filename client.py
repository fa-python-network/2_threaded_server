import socket

sock = socket.socket()
num_port = input("Input port number of server: ")
try:
    num_port = int(num_port)
except:
    num_port = 4448
    print("incorrect format of port number")
print("Connection to server")
sock.connect(('localhost', num_port))
client_name = input("Input your name: ")
if not client_name:
    client_name = "Client"
sock.send(client_name.encode())
while True:
    msg = input("Input a message to server: ")
    print("Sending data to server")
    sock.send(msg.encode())
    if msg == "exit":
        break


print("Taking data from server")
data = sock.recv(1024)

print("Disconnected with server")
sock.close()

print(data.decode())
