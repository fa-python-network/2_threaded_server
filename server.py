import errno
import socket
import errno
import sys


class Server(socket.socket):
    """Сервер"""

    def __init__(self):
        """Создание сокета"""
        super().__init__()
        self.sock = socket.socket()
        self.port = 9090
        self.host = ''
        self.users = {}

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
        """Подключение клиента"""
        while True:

            conn, addr = self.sock.accept()
            with open('log.txt', 'a') as file:
                print('Подключение клиента', file=file)

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

            self.chatting(conn)

    def chatting(self, conn):
        """Обмен сообщениями с клиентом"""
        while True:
            data = self.recv_msg(conn)
            with open('log.txt', 'a') as file:
                print('Приём данных от клиента', file=file)
            if not data:
                conn.close()
                break

            self.send_msg(data.upper(), conn)
            with open('log.txt', 'a') as file:
                print('Отправка данных клиенту', file=file)

        with open('log.txt', 'a') as file:
            print('Отключение клиента', file=file)




sock = Server()
sock.bind()
sock.get_users()
sock.listen(3)
sock.connecting()

