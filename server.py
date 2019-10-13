import socket
import threading

port = 9090
sock = socket.socket()


class T(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self):
        msg = ""
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            self.conn.send(data)
            print(data.decode())



port = 9090
try:
    sock.bind(('', port))
except OSError:
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    print(f"use port {port}")
sock.listen()
while True:
    conn, addr = sock.accept()
    print(addr)
    T(conn, addr).start()
conn.close()
