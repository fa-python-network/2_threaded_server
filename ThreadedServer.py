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
        self.data = ""
        self.lock = threading.Lock()
        self.get_users()
        self.work = True
        self.threads = []

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
        try:
            # При получении пустого сообщения (отключение клиента) сервер не должен крашиться
            length_msg = int(sock.recv(10).decode())
        except ValueError:
            return ''
        else:
            msg = sock.recv(length_msg).decode()
            return msg

    def close_server(self):
        """Закрытие сервера, используется для добавления соответствующей записи в лог файл при закрытии сервера через
        Ctrl+C """
        with open('log.txt', 'a') as file:
            print('Остановка сервера', file=file)
        self.work = False

        # на этом моменте у нас остался 1 незакрытый цикл
        # сервер всё ещё ждёт 1-го последнего подключения
        # так дадим ему то, чего он так ждёт

        client = socket.socket()
        client.connect(('localhost', server.port))
        self.send_msg('0', client)
        self.send_msg('close', client)
        self.recv_msg(client)
        self.send_msg('close', client)
        self.recv_msg(client)
        self.recv_msg(client)
        self.recv_msg(client)
        client.close()
        self.sock.close()

    def new_user(self, conn):
        """Добавление нового пользователя в файл users.txt"""
        name = self.recv_msg(conn)
        # Проверка незанятости имени
        if name not in self.users.keys():
            self.send_msg('1', conn)
            password = self.recv_msg(conn)
            self.users[name] = self.users.get(name, password)
            with open('users.txt', 'w') as users:
                print(self.users, file=users)
            return name
        else:
            self.send_msg('0', conn)
            flag2 = self.recv_msg(conn)
            if int(flag2):
                # Как и почему это должно писаться так я понял очень смутно
                # Но без этого может возвращаться пустое имя
                name = self.old_user(conn)
                return name
            else:
                name = self.new_user(conn)
                return name

    def old_user(self, conn):
        """Проверка пароля при входе старого пользователя"""
        name = self.recv_msg(conn)
        # Проверка есть ли такое имя
        if name in self.users.keys():
            self.send_msg('1', conn)
            passwd = self.users[name]
            while True:
                password = self.recv_msg(conn)
                if passwd == password:
                    self.send_msg('0', conn)
                    return name
                else:
                    self.send_msg('1', conn)
        else:
            self.send_msg('0', conn)
            flag2 = self.recv_msg(conn)
            if int(flag2):
                name = self.new_user(conn)
                return name
            else:
                name = self.old_user(conn)
                return name

    def bind(self, port):
        """Поиск незанятого порта и его прослушивание"""
        self.port = port
        self.host = ''
        flag = 1

        while flag:
            try:
                self.sock.bind((self.host, self.port))
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    if self.port <= 65535:
                        self.port += 1
                    else:
                        self.port = 9090
            else:
                flag = 0
        with self.lock:
            print("Слушаю порт: ", self.port)

        with open('log.txt', 'a') as file:
            print('Запуск сервера', file=file)

    def get_users(self):
        """Получение данных про всех старых клиентов"""
        # Это будет волшебный пользователь, благодря которому сервер сможет закрыться
        self.users = {'close': 'close'}
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
        while self.work:
            try:
                conn, addr = self.sock.accept()
            except OSError:
                break
            with open('log.txt', 'a') as file:
                print('Подключение клиента', file=file)
            thread = threading.Thread(target=self.chatting, name=str(addr[1]), args=[conn, addr])
            self.threads.append(thread)
            thread.start()

    def hello_user(self, conn):
        # Считывание имени клиеента и пароля
        flag = int(self.recv_msg(conn))
        if flag:
            name = self.new_user(conn)
        else:
            name = self.old_user(conn)

        msg = 'Hello ' + name + ' '
        self.send_msg(msg, conn)
        sent_data_count = len(self.data)
        self.data = self.data + '[' + name + ']: join chat\n'

        return sent_data_count, name

    def chatting(self, conn, addr):
        # Получаем счётчик чата и имя, идея так себе, но работает
        sent_data_count, name = self.hello_user(conn)

        recv = threading.Thread(target=self.chat_recv, name='recv' + str(addr[1]), args=[conn, name])
        send = threading.Thread(target=self.chat_send, name='send' + str(addr[1]), args=[conn, name, sent_data_count])
        self.threads.append(recv)
        self.threads.append(send)
        recv.start()
        send.start()

    def chat_recv(self, conn, name):
        while self.work:
            data = self.recv_msg(conn)
            if data == 'exit':
                self.data = self.data + '[' + name + ']: left chat\n'
                break

            elif data == 'close':
                conn.close()
                break

            with self.lock:
                with open('log.txt', 'a') as file:
                    print('Приём данных от клиента', file=file)
                self.data = self.data + '[' + name + ']: ' + data + '\n'

    def chat_send(self, conn, name, sent_data_count):
        # Я 2 недели разбирался с потоками, поэтому чат через очередь это слишком сложно
        # Пока сервер активен он хранит все сообщения которые к нему приходили
        # И отправляет их клиенту в зависимости от счётчика, который тоже как-то всрато работает
        while self.work:
            with self.lock:
                if len(self.data) > sent_data_count:
                    self.send_msg(self.data[sent_data_count:], conn)
                    if self.data[sent_data_count:] == '[' + name + ']: left chat\n':
                        self.send_msg('exit', conn)
                        break
                    with open('log.txt', 'a') as file:
                        print('Отправка данных клиенту', file=file)
                    sent_data_count = len(self.data)
        self.send_msg("close", conn)

    @staticmethod
    def show_logs():
        with open("log.txt", "r") as log:
            data = log.read()
            if data == "":
                data = "Логи пустые"
            print(data)

    @staticmethod
    def clear_logs():
        with open("log.txt", "w") as log:
            log.write("")
            print("Логи очищены")

    @staticmethod
    def clear_users():
        with open("users.txt", "w") as users:
            users.write("")


def work(server, port):
    try:
        server.bind(port)
        server.listen(3)
        server.connecting()
    except KeyboardInterrupt:
        server.close_server()


if __name__ == '__main__':
    server = Server()
    try:
        while True:
            try:
                port = int(input("Введите номер порта: "))
            except ValueError:
                print("Порт - целое число")
            else:
                break
        ChatThread = threading.Thread(target=work, args=[server, port])
        ChatThread.start()

        with server.lock:
            print("Возможности сервера:")
            print("Для показа логов введите: logs.show")
            print("Для удаления логов введите: logs.del")
            print("Для очистки файла идентификации введите: users.clear")
            print("Для паузы в прослушивании порта введите: server.pause")
            print("Для закрытия сервера введите: server.close")

        while True:
            action = input()
            if action == 'logs.show':
                Server.show_logs()
            elif action == 'logs.del':
                Server.clear_logs()
            elif action == 'users.clear':
                Server.clear_users()
            elif action == 'server.pause':
                print("Это я не придумал")
            elif action == 'server.close':
                server.close_server()
                break
    except KeyboardInterrupt:
        server.close_server()

