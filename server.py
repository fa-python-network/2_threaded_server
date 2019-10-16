import socket

import threading
import json

sock = socket.socket()
history = {}


##'users.json'
def write_into_json(dct, file_name):
    with open(file_name, 'w') as f:
        json.dump(dct, f)

def read_from_json(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)


def send_msg(conn, msg):
    header = f'{len(msg):<4}'
    conn.send(f'{header}{msg}'.encode())


def recv_msg(conn):
    header = int(conn.recv(4).decode().strip())
    data = conn.recv(header*2).decode()
    return data


class T(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self):


        name = recv_msg(self.conn)
        pr = True
        try:
            ex_name = users[name]
        except KeyError:
            pr = False
        send_msg(self.conn, str(pr))
        while not pr:
            name = recv_msg(self.conn)
            pr = True
            try:
                ex_name = users[name]
            except KeyError:
                pr = False
            send_msg(self.conn, str(pr))



        pr = False
        pswd = recv_msg(self.conn)
        if ex_name == pswd:
            pr = True
        send_msg(self.conn, str(pr))
        while not pr:
            pswd = recv_msg(self.conn)
            if ex_name == pswd:
                pr = True
            send_msg(self.conn, str(pr))

        msg = ""
        while True:
            try:
                data = recv_msg(self.conn)
            except ValueError:
                break
            send_msg(self.conn, data)
            print(data)



port = 9090
users = read_from_json('users.json')
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
