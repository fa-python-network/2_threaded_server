import socket
import threading

sock = socket.socket()
sock.bind(('', 9093))
sock.listen(1000)

def client(conn, addr):
    msg = ''
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg += data.decode()
        conn.send(data)

    conn.close()

while True:
    conn, addr = sock.accept()
    p1 = threading.Thread(target=client, args=(conn, addr))
    p1.start()
