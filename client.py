# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 09:20:29 2019

@author: 184136
"""

from socket import socket


sock = socket()
host, port = 'localhost', 8000
connected = False

try:
    sock.connect((host, port))
    connected = True
except ConnectionError:
    print("Unreachable server")

if connected:
    print(f"Connected to {host}:{port}")

    msg = input('Enter your message: ')
    sent = False
    try:
        sock.send(msg.encode())
        sent = True
    except ConnectionError:
        print('Sending error')

    if sent:
        print(f'Message "{msg}" sent to {host}:{port}')

        answer = b''
        while True:
            chunk = sock.recv(1024)
            answer += chunk
            if not chunk:
                break

        print(f'"{answer.decode()}" returned by server')

sock.close()

input('Press Enter to exit...')
