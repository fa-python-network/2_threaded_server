import threading
import socket
import errno
import sys
import time


class Server(socket.socket):
    """Сервер"""

    def __init__(self):
        """Создание сокета"""
        super().__init__()
        self.sock = socket.socket()
        self.port = 9090
        self.host = ''
        self.users = {}
        self.threads = []
        self.data = ""
        self.lock = threading.Lock()

    @staticmethod
    def send_msg(msg, sock):
        """Отправка сообщения с добавлением длины сообщения"""
        length_msg = str(len(msg))
        length_msg = '0' * (10 - len(length_msg)) + length_msg
        msg = length_msg + msg
        sock.send(msg.encode())

    @staticmethod
    def recv_msg(sock):
        """Получение сообщения с учётом его длины"""
        # При получении пустого сообщения (отключение клиента) сервер не должен крашиться
        try:
            length_msg = int(sock.recv(10).decode())
        except ValueError:
            msg = None
        else:
            msg = sock.recv(length_msg).decode()
        return msg

    def close_server(self):
        """Закрытие сервера, используется для добавления соответствующей записи в лог файл при закрытии сервера через
        Ctrl+C """
        with open('log.txt', 'a') as file:
            print('Остановка сервера', file=file)
        self.sock.close()
        sys.exit()

    def new_user(self, conn, addr, d):
        """Добавление нового пользователя в файл users.txt"""
        name = self.recv_msg(conn)
        password = self.recv_msg(conn)
        d[addr[0]] = d.get(addr[0], [name, password])
        with open('users.txt', 'w') as users:
            print(d, file=users)

    def old_user(self, conn, addr, d):
        """Проверка пароля при входе старого пользователя"""
        passwd = d[addr[0]][1]
        password = self.recv_msg(conn)
        if passwd == password:
            self.send_msg('0', conn)
            self.recv_msg(conn)
            return
        else:
            self.send_msg('1', conn)
            self.old_user(conn, addr, d)

    def bind(self):
        """Поиск незанятого порта и его прослушивание"""
        flag = 1

        while flag:
            try:
                self.sock.bind((self.host, self.port))
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    self.port += 1
            else:
                flag = 0
        print(self.port)

        with open('log.txt', 'a') as file:
            print('Запуск сервера', file=file)

    def get_users(self):
        """Получение данных про всех старых клиентов"""
        # Пытаемся прочесть данные из файла и преобразовать их в словарь
        try:
            with open('users.txt', 'r') as users:
                self.users = eval(users.read())
        # Если файла нет: создаём его, список юзеров - пустой словарь
        except FileNotFoundError:
            with open('users.txt', 'w') as users:
                pass
        # Если файл пустой: список юзеров - пустой словарь
        except SyntaxError:
            pass

    def listen(self, count):
        self.sock.listen(count)

        with open('log.txt', 'a') as file:
            print('Начало прослушивания порта', file=file)

    def connecting(self):
        thread = threading.Thread(target=self.connecting)
        self.threads.append(thread)
        """Подключение клиента"""
        conn, addr = self.sock.accept()
        with open('log.txt', 'a') as file:
            print('Подключение клиента', file=file)

        thread.start()

        self.hello_user(conn, addr)

    def hello_user(self, conn, addr):
        # Считывание имени клиеента и пароля
        if addr[0] not in self.users.keys():
            flag = str(1)
            self.send_msg(flag, conn)
            self.new_user(conn, addr, self.users)
        else:
            flag = str(0)
            self.send_msg(flag, conn)
            self.old_user(conn, addr, self.users)

        msg = 'Hello ' + self.users[addr[0]][0]
        self.send_msg(msg, conn)

        self.chatting(conn, addr)

    def chatting(self, conn, addr):
        """Обмен сообщениями с клиентом"""

        send = threading.Thread(target=self.chat_send, args=[conn])
        recv = threading.Thread(target=self.chat_recv, args=[conn, addr])

        send.start()
        recv.start()

    def chat_recv(self, conn, addr):
        while True:
            data = self.recv_msg(conn)
            with open('log.txt', 'a') as file:
                print('Приём данных от клиента', file=file)
            self.data = self.data + '[' + self.users[addr[0]][0] + ']: ' + data + '\n'

    def chat_send(self, conn):
        sent_data_count = len(self.data)
        while True:
            with self.lock:
                if len(self.data) > sent_data_count:
                    self.send_msg(self.data[sent_data_count:], conn)
                    with open('log.txt', 'a') as file:
                        print('Отправка данных клиенту', file=file)
                    sent_data_count = len(self.data)


sock = Server()
try:
    sock.bind()
    sock.get_users()
    sock.listen(3)
    while True:
        sock.connecting()
except KeyboardInterrupt:
    sock.close_server()
