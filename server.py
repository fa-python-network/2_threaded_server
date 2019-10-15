import socket
from threading import Thread


def connclient(conn, addr):
    client_name = conn.recv(1024)
    while True:
        data = conn.recv(1024)
        if not data:
            return
        if data.decode() == "exit":
            conn.close()
            print("Клиент " + client_name.decode() + " отключился")
            return
        conn.send(data)


sock = socket.socket()
num_port = input("Input port number to start a server: ")
try:
    num_port = int(num_port)
except ValueError:
    num_port = 4448
except OSError:
    num_port += 11
sock.bind(('', num_port))
print("Server is running on port " + str(num_port) + "\n")

while True:
    stp = input("If you want to shutdown server, print 'exit', NO? Press other keys")
    if stp == 'exit':
        sock.close()
        break
    sock.listen(1)
    conn, addr = sock.accept()
    Thread(target=connclient, args=(conn, addr)).start()
