import socket
import hashlib
import json
import logging
from sendcheck import *
import threading

SALT = 'memkekazazaaaff'.encode("utf-8")  # соль для хеширования
varcom = ['logs', 'stop', 'logsclr', 'nameclr']  # Список доступных команд
users = []
# Настройки логгинга (( Взято у умного соседа))
logging.basicConfig(filename="log_serv", level=logging.INFO)

with open('names.json', 'r') as file:
    names = json.load(file)


def serv_work(sock):
    print('Сервер работает.')
    print('Список доступных комманд:')
    print(varcom)
    main = True
    while main:
        command = input()
        if command not in varcom:
            print('Нет такой команды.')
        elif 'logs' == command:
            with open('log_serv', 'r') as file:
                for raw in file:
                    print(raw)
        elif 'logclr' == command:
            with open('log_serv', 'w') as file:
                pass
        elif 'nameclr' == command:
            with open('names.json', 'w') as file:
                json.dump({}, file)
        elif 'stop' == command:
            main = False
            sock.close()


def potok_accept():
    while True:
        try:
            potok = BugurtThread(*sock.accept())
            potok.start()
        except:
            break


def hashpass(passw: str):  # Функция хеширования данных
    return hashlib.sha512(passw.encode("utf-8") + SALT).hexdigest()


# Начало и инициализация потока пользователя.
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

    def login(self):  # поток авторизации пользователя.
        try:
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
            sendmsg(
                self.conn, "Здесь сегодня тесновато. Но для тебя всегда место найдется!")
        except ConnectionResetError:
            pass

    def sendall(self, msg):
        for con in users:
            sendmsg(con.conn, self.username+': '+msg)
            with open('story.json', 'a') as file:
                json.dump(self.username+': '+msg+'\n', file)

    def run(self):  # Поток чата.
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


work = threading.Thread(target=serv_work, args=[sock])
work.start()
main = True

while main:  # main цикл обрабатывает команды сервера.
    try:
        potok = BugurtThread(*sock.accept())
        potok.start()
    except OSError:
        print('Сервер закрыт.')
        break

