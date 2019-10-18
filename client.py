import socket
import threading

def accept_msg():
    while True:
        msg = sock.recv(1024).decode()
        print(msg)


sock = socket.socket()

while True:
    ip = '127.0.0.1'#input('Enter the ip: ')
    port = 9090#int(input('Enter the port: '))
    try:
        sock.connect((ip, port))
        break
    except ConnectionError:
        print("Error. Try again")


rcv = threading.Thread(target=accept_msg)
rcv.start()
while True:
    msg = input()
    if msg in ['exit', 'q']:
        break
    sock.send(msg.encode())

sock.close()







