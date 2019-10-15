import logging as log
import socket
from re import match
import json
import threading

log.basicConfig(filename='server.txt', level=log.DEBUG)


def send(conn, message):
    header = len(message)
    full_message = f'{header:4}{message}'.encode()
    conn.send(full_message)


def receive(conn):
    header = conn.recv(4).decode()
    message = conn.recv(int(header))
    return message.decode()


def identify(conn, addr):
    with open('identify.json', 'r') as f:
        data = json.load(f)
    if not addr[0] in data:
        send(conn, 'What is your name?')
        info = receive(conn)
        data[addr[0]] = info
    send(conn, f'Hello, {data[addr[0]]}')
    with open('identify.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def handle_client(conn):
    while 1:
        identify(conn, addr)
        received_msg = receive(conn)
        send(conn, received_msg)
        if not received_msg:
            log.info('Разрыв соединения')
            conn.close()
            return


sock = socket.socket()
log.info('Запуск сервера')
host = 'localhost'
port = 135  # 9090
host_ = input('Host: ')
port_ = input('Port:')
host_regex = r'[0-2]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-2]?[0-9]?[0-9]'
if host_ and match(host_regex, host_):
    host = host_
print(f'current host:{host}')
if port_.isdigit() and 1024 <= int(port_) <= 65535:
    port = int(port_)

try:
    sock.bind(('', port))
except OSError:
    sock.bind(('', 0))
    port = sock.getsockname()[1]

log.debug('Сервер слушает порт {}'.format(port))
print(f'current port.py: {port}')
sock.listen(5)

try:
    while 1:
        conn, addr = sock.accept()
        log.info('Подключен клиент {}:{}'.format(*addr))
        threading.Thread(target = handle_client, args = [conn]).start()
finally:
    log.info('Сервер завершает работу')
    sock.close()
