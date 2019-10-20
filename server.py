import socket
import hashlib
import json
#import uuid
import logging
import threading
from time import sleep
commands = ['Показ логов', 'Очистка логов', 'Очистка файла идентификации', 'Остановка сервера']
commands_short = ['showlogs','clrlogs','clrID','stop']
users = []

logging.basicConfig(filename="serv.log", level=logging.INFO)
with open('users.json', 'r') as file:
    names = json.load(file)


def sendmsg(who, msg):
    sleep(0.1)
    msg_len = str(len(msg))
    while len(msg_len) < 5:
        msg_len = msg_len + "+"
    who.send((msg_len + msg).encode())


def checkmsg(who):
    msg_len = who.recv(5).decode()
    if msg_len == "":
        return ""
    msg_len = int(msg_len.replace('+', ''))
    msg = who.recv(msg_len*2).decode()
    return msg

def serv_work(sock):
    print('Сервер работает.')
    print('Список доступных комманд:')
    for i in range(len(commands)):
        print(f"{i+1}. {commands[i]}: \"{commands_short[i]}\"")

    while True:
        command = input()
        if command not in commands_short:
            print('Нет такой команды.')
        elif 'showlogs' == command:
            with open('serv.log', 'r') as file:
                for raw in file:
                    print(raw)
        elif 'clrlogs' == command:
            with open('serv.log', 'w') as file:
                pass
            print("Выполнено")
        elif 'clrID' == command:
            with open('users.json', 'w') as file:
                json.dump({}, file)
            print("Выполнено")
        elif 'stop' == command:
            sock.close()
            break


def potok_accept():
    while True:
        try:
            potok = ConnectionThread(*sock.accept())
            potok.start()
        except:
            break


Salt = 'postfixforpassw'.encode("utf-8")


def hashpassword(passw: str):  # Функция хеширования данных
    return hashlib.sha512(passw.encode("utf-8") + Salt).hexdigest()
# Начало и инициализация потока пользователя.


class ConnectionThread(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.username = ''
        self.connected = True
        self.login()
    @staticmethod
    def ifIpInBase(ipv):  # Функция проверки ip адреса в базе
        if ipv not in names:
            return False
        else:
            return names[ipv][0]
    @staticmethod
    def autoriz(ipv, passw):
        if names[ipv][1] == hashpassword(passw):
            return True
        else:
            return False

    def login(self):  # поток авторизации пользователя.
        try:
            logging.info(f"Connect with - {self.addr}")
            check = self.ifIpInBase(self.addr[0])
            access = False
            if check:  # зарегистрированный пользователь
                msg = f'Добрый день, {check}! \nВведите пароль:'
                while not access:
                    sendmsg(self.conn, msg)
                    passw = checkmsg(self.conn)
                    access = self.autoriz(self.addr[0], passw)
                    msg = 'Неверный ввод!'
                sendmsg(self.conn, 'Добро пожаловать!')
            else:  # незарегистрированный пользователь
                sendmsg(self.conn, "Добро пожаловать в наш чат! Пожалуйста, пройдите регистрацию.\nВведите имя:")
                name = checkmsg(self.conn)
                check = name
                sendmsg(self.conn, "Придумайте пароль:")
                passw = checkmsg(self.conn)
                names[self.addr[0]] = [name, hashpassword(passw)]
                with open('users.json', 'w') as file:
                    json.dump(names, file)
            self.username = check
            sendmsg(self.conn, "\nПрисоединяйся к нашей беседе! Ну а если спешишь по делам, то отправь \"exit\" в чат, чтобы выйти.")
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
while True:
    port = input('Введите номер порта от 1024 до 49151: \n')
    port = int(port)
    if 1023 < port < 49152:
        break
    else:
        print('Неверный номер порта.')

tryconnection = True
while tryconnection:  # Обработка подключения к порту
    try:
        sock.bind(('', port))
        tryconnection = False
    except:
        port += 1

print(f"Слушается {port} порт")
sock.listen(4)


work = threading.Thread(target=serv_work, args=[sock])
work.start()
main = True

while main:  # main цикл обрабатывает команды сервера.
    try:
        potok = ConnectionThread(*sock.accept())
        potok.start()
    except OSError:
        print('Сервер закрыт.')
        break
