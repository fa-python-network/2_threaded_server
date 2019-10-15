import socket
import logging as log

log.basicConfig(filename='log.txt', level=log.DEBUG)


def send(conn, message):
    header = str(len(message))
    full_message = f'{header:4}{message}'.encode()
    conn.send(full_message)


def receive(conn):
    header = conn.recv(4).decode()
    message = conn.recv(int(header))
    return message.decode()


def identify(sock):
    data = receive(sock)
    if data == 'What is your name?':
        name = input(data)
        send(sock, name)
        data = receive(sock)
    print(data)


sock = socket.socket()
log.info('Клиент запущен')
sock.connect(('localhost', int(input("vvedite port: "))))
log.info('Подключено к серверу')
identify(sock)
msg=''
while msg != 'exit':
    msg = input()
    log.info('Отправляю сообщение {}'.format(msg))
    send(sock, msg)
    log.info('Получаю ответ сервера')
    received_msg = receive(sock)
    print(received_msg)
sock.close()
