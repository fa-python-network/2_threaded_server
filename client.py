import socket

sock = socket.socket()

sock.connect(('localhost', 9092))
msg = ''

while msg != 'exit':
    msg = input('->')
    sock.send(msg.encode())
    data = sock.recv(1024)
    print("ANSWER:", data.decode())


sock.close()
