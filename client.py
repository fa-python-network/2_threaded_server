# login:    vladik
# pwd:      12345
# sendto name msg

import socket
import logging as log
from re import match
from strings import *

ENCODING = 'cp1251'

log.basicConfig(filename='client.log', format='%(filename)s [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=log.DEBUG)


class Client:

    ADDRESS = 'localhost'
    PORT = 9797
    HOST_REGEX = r'[1-2]?[0-9]{1, 2}\.[1-2]?[0-9]{1, 2}\.[1-2]?[0-9]{1, 2}\.[1-2]?[0-9]{1, 2}'
    RUNNING = True
    MAX_CONN = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.debug('Socket started')
        self.addr, self.port = self.ask_addr()
        try:
            self.sock.connect((self.addr, self.port))
            log.info(f'Sucessfully connected to {self.addr}:{self.port}')
            self.auth()
            self.receive_messages()
            self.mainloop()
        finally:
            self.sock.close()


    def ask_addr(self):
        address_ = input(f'Address (empty for \'{self.ADDRESS}\'): ')
        port_ = input(f'Port (empty for {self.PORT}): ')
        return address_ if address_ and match(self.HOST_REGEX, address_) else self.ADDRESS, int(port_) if port_ and '1024' <= port_ <= '65535' else self.PORT

    
    def send(self, msg):
        assert len(msg) <= 1020
        header = f'{len(msg):<4}'
        log.info(f'Sending {header}{msg}')
        self.sock.send(f'{header}{msg}'.encode(ENCODING))

    def recv(self):
        header = int(self.sock.recv(4).decode(ENCODING).strip())
        received =  self.sock.recv(header).decode(ENCODING)
        log.info(f'Received {received}')
        return received
    
    def auth(self):
        logged_in = False
        while not logged_in:
            uname = input(self.recv())
            self.send(uname)
            pwd = input(self.recv())
            self.send(pwd)
            result = self.recv()
            if result == successful_login:
                logged_in = True
            print(self.recv())
        log.info('Sucessfully logged in')

    def receive_messages(self):
        log.info('Receiving held messages')
        msg = self.recv()
        flag = False
        while msg != end_of_messages:
            print('Msg from {}: {}'.format(msg[:16].strip(), msg[16:]))
            msg = self.recv()
            flag = True
        if not flag:
            log.debug('No held messages')
            print('No new messages for you')
        

    def mainloop(self):
        msg = ''
        while msg != 'exit':
            msg = input('<= ')
            self.send(msg)
            print('=>', self.recv())



Client()
            
