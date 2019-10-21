import socket
import threading
import sys
import select


class Client(socket.socket):
    """Клиент"""

    def __init__(self):
        """я задоллбался писать эти комментарии и так вроде всё понятно"""
        super().__init__()
        self.sock = socket.socket()
        self.lock = threading.Lock()
        self.client_work = True

    @staticmethod
    def send_msg(msg, sock):
        length_msg = str(len(msg))
        length_msg = '0' * (10 - len(length_msg)) + length_msg
        msg = length_msg + msg
        sock.send(msg.encode())

    @staticmethod
    def recv_msg(sock):
        length_msg = int(sock.recv(10).decode())
        msg = sock.recv(length_msg).decode()
        return msg

    def new_user(self, name):
        self.send_msg(name, self.sock)
        # Проверка незанятости данного имени 1 - свободно, 0 - занято.
        flag = self.recv_msg(self.sock)
        if int(flag):
            while True:
                print("Введите пароль")
                password = input()
                print("Повторите пароль")
                password2 = input()
                if password == password2:
                    break
            self.send_msg(password, self.sock)
        else:
            print("Данное имя уже занято")
            print("Чтобы войти под этим именем введите 1")
            print("Чтобы ввести другое имя введите 0")
            flag2 = int(input())
            self.send_msg(str(flag2), self.sock)
            if flag2:
                self.old_user(name)
            else:
                name = input("Введите ваше имя: ")
                self.new_user(name)

    # Это не безопасно, но мне лень делать что-то другое, ибо я тупенький)
    def old_user(self, name):
        self.send_msg(name, self.sock)
        # Если 1 - имя есть, если 0 - это имя ещё не зарегестрированно
        flag = self.recv_msg(self.sock)
        if int(flag):
            while True:
                password = input("Введите пароль: ")
                self.send_msg(password, self.sock)
                flag = self.recv_msg(self.sock)
                if not int(flag):
                    break
        else:
            print("Такого имени не существует")
            print("Для регистрации под этим именем введите 1")
            print("Чтобы ввести другое имя введите 0")
            flag2 = int(input())
            self.send_msg(str(flag2), self.sock)
            if flag2:
                self.new_user(name)
            else:
                name = input("Введите ваше имя: ")
                self.old_user(name)

    def connection(self):
        self.host = input('Введите имя хоста или нажмите Enter для использования значения по умолчанию ')
        port = input('Введите номер порта или нажмите Enter для использования значения по умолчанию ')

        if self.host == '':
            self.host = 'localhost'
        if port == '':
            self.port = 9090
        else:
            self.port = int(port)

        self.sock.connect((self.host, self.port))
        print('Соединение с сервером')

    def login(self):
        # Регистрация или Вход в акк
        print("Привет :)")
        print("Для регистрации введите 'R'")
        print("Для авторизации введите 'L'")
        while True:
            data = input()
            if data == 'R':
                self.send_msg('1', self.sock)
                print("Введите ваше имя: ")
                name = input()
                self.new_user(name)
                break
            elif data == 'L':
                self.send_msg('0', self.sock)
                name = input('Введите ваше имя: ')
                self.old_user(name)
                break
            else:
                print("Попробуйте ещё раз")

    def chatting(self):
        self.login()

        send = threading.Thread(target=self.chat_send)
        recv = threading.Thread(target=self.chat_recv)
        send.start()
        recv.start()

        print('Для отключения от сервера введите exit')

    def chat_recv(self):
        while True:
            data = self.recv_msg(self.sock)
            with self.lock:
                if data == 'exit':
                    self.sock.close()
                    break
                elif data == 'close':
                    self.send_msg('close', self.sock)
                    # 1 раз закроет поток рассылки сообщений, а вот зачем нужно жать ещё 1 enter я так и не понял
                    print("Сервер временно не работает\nЧтобы закрыть клиент дважды нажмите enter")
                    break
                print(data[:-1])

    def chat_send(self):
        while True:
            msg = input()
            with self.lock:
                try:
                    self.send_msg(msg, self.sock)
                except ConnectionAbortedError:
                    self.sock.close()
                    break
            if msg == 'exit':
                break


client = Client()
try:
    client.connection()
    client.chatting()
except:
    client.client_work = False
