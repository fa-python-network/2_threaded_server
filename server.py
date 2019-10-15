import socket
from re import match
import logging as log
from threading import Thread
from json import load, dump
from hashlib import md5
from strings import *

ENCODING = 'cp1251'

log.basicConfig(
                format='%(filename)s [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=log.DEBUG)


class Server:

    ADDRESS = ''
    PORT = 9797
    HOST_REGEX = r'[1-2]?[0-9]{1, 2}\.[1-2]?[0-9]{1, 2}\.[1-2]?[0-9]{1, 2}\.[1-2]?[0-9]{1, 2}'
    RUNNING = True
    MAX_CONN = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.debug('Socket created')
        self.addr, self.port = self.ask_addr()
        self.bind()
        log.debug(f'Socket binded to port {self.port}')
        self.sock.listen(self.MAX_CONN)
        log.debug(f'Socket is listening {self.MAX_CONN} connections')
        self.mainloop()

    def mainloop(self):
        try:
            while 1:
                conn, addr = self.sock.accept()
                log.info(f'Connected {addr}')
                Thread(target=self.handle_client, args=(conn,)).start()
        finally:
            log.info('Server is closing')
            self.sock.close()

    def send(self, conn, msg):
        assert len(msg) <= 1020
        header = f'{len(msg):<4}'
        conn.send(f'{header}{msg}'.encode(ENCODING))
        log.debug(f'Sended msg: {msg}')

    def recv(self, conn):
        try:
            header = int(conn.recv(4).decode(ENCODING).strip())
        except ValueError:
            conn.close()
            return 'Connection closed'
        data = conn.recv(header).decode(ENCODING)
        log.debug(f'Received msg: {data}')
        return data

    def ask_addr(self):
        address_ = input(f'Address (empty for \'{self.ADDRESS}\'): ')
        port_ = input(f'Port (empty for {self.PORT}): ')
        return address_ if address_ and match(self.HOST_REGEX, address_) else self.ADDRESS, port_ if port_ and '1024' <= port_ <= '65535' else self.PORT

    def bind(self):
        try:
            self.sock.bind((self.addr, self.port))
        except OSError:
            self.sock.bind((self.addr, 0))
            self.port = self.sock.getsockname()[1]
            print(f'New PORT is {self.port}')

    def auth(self, conn):
        logged_in = False
        while not logged_in:
            self.send(conn, ask_username)
            uname = self.recv(conn)
            self.send(conn, ask_password)
            pwd = self.recv(conn)
            with open('users.json', 'r', encoding='utf-8') as f:
                users = load(f)
            if users.get(uname) == md5(pwd.encode()).hexdigest():
                self.send(conn, successful_login)
                logged_in = True
                log.debug(f'Successful login: {uname}')
                self.send(conn, greetings.format(uname))
            else:
                log.debug(f'Incorrect login: {uname}')
                self.send(conn, incorrect_password)
                self.send(conn, incorrect_password)
        return uname


    def send_messages(self, conn, uname):
        with open('messages.json') as f:
            data = load(f)
        if not uname in data:
            self.send(conn, end_of_messages)
            return
        for msg in data[uname]:
            self.send(conn, f"{msg[0]:16}{msg[1]}")
        data[uname] = []
        with open('messages.json', 'w') as f:
            dump(data, f, ensure_ascii=False)
        self.send(conn, end_of_messages)


    def handle_client(self, conn):
        uname = self.auth(conn)
        self.send_messages(conn, uname)
        while 1:
            data = self.recv(conn)
            if data.startswith('sendto'):
                data = data.split()
                if not len(data) >= 3:
                    self.send(conn, unresolved_command)
                    continue
                to = data[1]
                msg = ' '.join(data[2:])
                with open('users.json') as f:
                    users = load(f).keys()
                if not to in users:
                    self.send(conn, no_user)
                    continue
                with open('messages.json', 'r') as f:
                    msgs = load(f)
                msgs.setdefault(to, []).append([uname, msg])
                with open('messages.json', 'w') as f:
                    dump(msgs, f, ensure_ascii=False)
                self.send(conn, 'Success')
            else:
                if data == 'Connection closed':
                    break
                self.send(conn, data)


Server()
