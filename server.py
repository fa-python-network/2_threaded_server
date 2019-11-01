# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 09:21:44 2019

@author: 184136
"""

from socket import socket
from threading import Thread


def main():
    def handle_client(conn, addr):
        data = b''
        while True:
            chunk = conn.recv(1024)
            data += chunk
            if len(chunk) < 1024:
                break

        text = data.decode()
        print(f'Sever have got "{text}" from {addr}')

        conn.send(data)
        print(f'{data} sent back to client')

        conn.close()
        print(f'Connection with {addr} finished')

    while True:
        conn, addr = sock.accept()
        addr = addr[0]
        print(f'New client "{addr}" connected')

        new_client_handler = Thread(target=handle_client, args=(conn, addr))
        new_client_handler.start()


sock = socket()
print('Server started here')

host, port = '', 8000

sock.bind((host, port))
sock.listen(5)
print('Port listening started')

main()

sock.close()

print('Server stopped')
