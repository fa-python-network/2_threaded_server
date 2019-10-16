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

        #try:
            #c = users[self.addr]
        #except KeyError:
            #send_msg(self.conn, "What is your name?")
            #users[self.addr] = []
            #users[self.addr].append(recv_msg(self.conn))
            #users[self.addr].append(recv_msg(self.conn))
           #write_into_json(users, 'users.json')

        #send_msg(self.conn, users[self.addr][0])
        #send_msg(self.conn, users[self.addr][1])
        msg = ""
        while True:
            try:
                data = recv_msg(self.conn)
            except ValueError:
                break
            send_msg(self.conn, data)
            print(data)



port = 9090
#users = read_from_json('users.json')
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
