import socket
def new_sock(port, host):
    sock = socket.socket()
    try:
        sock.connect((host, port))
        print(f"Порт {port} свободен")
    except OSError:
        print(f"Порт {port} занят")
    sock.close()

print("Host:")
host = input()
if host == "":
    host = 'localhost'

for i in range(1,65536):
    new_sock(i, host)