import socket
import hashlib
import json
import logging
from sendcheck import *
import threading

SALT = 'memkekazazaaaff'.encode("utf-8")  # соль для хеширования
varcom = ['mymsg', 'send', 'exit']  # Список доступных команд
users = []
# Настройки логгинга (( Взято у умного соседа))
logging.basicConfig(filename="log_serv", level=logging.INFO)

with open('names.json', 'r') as file:
    names = json.load(file)


def hashpass(passw: str):  # Функция хеширования данных
    return hashlib.sha512(passw.encode("utf-8") + SALT).hexdigest()


class BugurtThread(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.username = ''
        self.connected = True
        self.login()

    @staticmethod
    def mem(ipv):  # Функция проверки ip адреса в базе
        if ipv not in names:
            return False
        else:
            return names[ipv][0]

    @staticmethod
    def autoriz(ipv, passw):  # Функция проверки пароля
        if names[ipv][1] == hashpass(passw):
            return True
        else:
            return False

    def login(self):
        logging.info(f"Connect - {self.addr}")
        check = self.mem(self.addr[0])
        access = False
        if check:  # Ветка знакомого пользователя
            msg = f'Добрый вечер, {check}! Ваш пароль?'
            while not access:
                sendmsg(self.conn, msg)
                passw = checkmsg(self.conn)
                access = self.autoriz(self.addr[0], passw)
                msg = 'Неверный ввод!'
            sendmsg(self.conn, 'ДАРОВА')
        else:  # Ветка нового пользователя
            sendmsg(self.conn, "Введите, ваше имя:")
            name = checkmsg(self.conn)
            check = name
            sendmsg(self.conn, "Введите, ваш пароль:")
            passw = checkmsg(self.conn)
            names[self.addr[0]] = [name, hashpass(passw)]
            with open('names.json', 'w') as file:
                json.dump(names, file)
        self.username = check
        sendmsg(self.conn, "Здесь сегодня тесновато. Но для тебя всегда место найдется!")

    def sendall(self, msg):
        for con in users:
            sendmsg(con.conn, self.username+': '+msg)

    def run(self):
        users.append(self)
        while self.connected:
            try:
                msg = checkmsg(self.conn)
                if msg == 'exit':
                    self.connected = False
                    users.remove(self)
                    logging.info(f'Command {msg}')
                else:
                    self.sendall(msg)
            except KeyboardInterrupt:
                break

sock = socket.socket()
port = 9090
portmiss = True
adress = ['localhost', '192.168.0.101']

while portmiss:  # Обработка подключения к порту
    try:
        sock.bind((adress[0], port))
        portmiss = False
    except:
        port += 1
sock.listen(4)
command = ("exit")  # Команды для логгинга


main = True
while main:  # main цикл обрабатывает команды клиента
    potok = BugurtThread(*sock.accept())
    potok.start()
