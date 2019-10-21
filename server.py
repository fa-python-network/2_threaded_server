import socket
import threading


class Server(socket.socket):
    def __init__(self):
        super().__init__()
        self.chat = ''
        self.sock = socket.socket()
        self.lock = threading.Lock()
        self.file = 'log_file_server.txt'
        self.get_users()
        self.history_count = 0

    # Функция для отправки сообщений
    def msg_s(self, msg, conn):
        length_msg = str(len(msg))
        length_msg = '0' * (10 - len(length_msg)) + length_msg
        msg = length_msg + msg
        conn.send(msg.encode())

    # Функция для получения сообщений
    def msg_r(self, conn):
        try:
            length_msg = int(conn.recv(10).decode())
        except ValueError:
            msg = None
        else:
            msg = conn.recv(length_msg).decode()
        return msg

    def history(self):
        with open("history.txt", 'a') as h:
            with self.lock:
                h.write(self.chat[self.history_count:])
                self.history_count = len(self.chat)

    def show_logs(self):
        with open(self.file, "r") as log:
            data = log.read()
            if data == "":
                data = "Логи отсутствуют"
            print(data)

    def clear_logs(self):
        with open(self.file, "w") as log:
            log.write("")
            print("Логи удалены")

    def clear_users(self):
        with open("users.txt", "w") as users:
            users.write("")
            print("Данные пользователей удалены")

    def new_user(self, conn, name):
        self.msg_s('1', conn)
        passwd = self.msg_r(conn)
        self.users[name] = self.users.get(name, passwd)
        with open('users.txt', 'w') as file:
            print(self.users, file=file)

    def old_user(self, conn, name):
        self.msg_s('0', conn)
        passwd = self.users[name]
        while True:
            p = self.msg_r(conn)
            if p == passwd:
                self.msg_s('0', conn)
                break
            self.msg_s('1', conn)

    def get_users(self):
        try:
            with open('users.txt', 'r') as users:
                self.users = eval(users.read())
        except FileNotFoundError:
            with open('users.txt', 'w') as users:
                self.users = {}
        except SyntaxError:
            self.users = {}

    def bind(self, port=9090):
        self.port = port
        while True:
            try:
                self.sock.bind(('', self.port))
            except:
                self.port += 1
            else:
                with open(self.file, 'a') as f:
                    f.write('Запуск сервера\n')
                break

    def listen(self, n=1):
        self.sock.listen(n)

        with open(self.file, 'a') as f:
            f.write(f'Начало прослушивания порта {self.port}\n')
        print(f'Слушаю порт с номером {self.port}')

    def connecting(self):
        while True:
            conn, addr = self.sock.accept()
            t = threading.Thread(target=self.work_with_client, args=[addr, conn])
            t.start()

    # Функция для работы с подключённым клиентом
    def work_with_client(self, addr, conn):
        name = self.msg_r(conn)
        if name in self.users.keys():
            self.old_user(conn, name)
        else:
            self.new_user(conn, name)

        msg = 'Hello ' + name + ' '
        self.msg_s(msg, conn)
        count = len(self.chat)
        self.chat = self.chat + name + ' -> join chat\n'

        with open(self.file, 'a') as f:
            f.write(f'Подключился клиент с {addr}\n')

        t1 = threading.Thread(target=self.chat_recv, args=[conn, name, addr])
        t2 = threading.Thread(target=self.chat_send, args=[conn, name, addr, count])
        t1.start()
        t2.start()

    # Получение данных для чата
    def chat_recv(self, conn, name, addr):
        while True:
            data = self.msg_r(conn)
            with open(self.file, 'a') as f:
                f.write(f'Получаю данные от {addr}\n')
            if data == 'exit':
                self.chat = self.chat + name + ' <- left chat\n'
                break
            self.chat += name + ' : ' + data + '\n'

    # Рассылка сообщений из чата
    def chat_send(self, conn, name, addr, count):
        while True:
            if len(self.chat) > count:
                data = self.chat[count:]
                count = len(self.chat)
                self.msg_s(data, conn)
                if data == name + ' <- left chat\n':
                    self.msg_s('close', conn)
                    break

            with open(self.file, 'a') as f:
                f.write(f'Отправляю данные {addr}\n')


def main(server, port):
    server.bind(port)
    server.listen()
    server.connecting()


if __name__ == '__main__':
    server = Server()
    port = int(input("Введите номер порта: "))
    t = threading.Thread(target=main, kwargs={'server': server, 'port': port})
    t.start()
    while True:
        event = input('a - показать логи\ns - удалить логи\nd - очистить файл идентификации\nw - записать историю '
                      'сообщений\n')
        if event == 'a':
            server.show_logs()
        elif event == 's':
            server.clear_logs()
        elif event == 'd':
            server.clear_users()
        elif event == 'w':
            server.history()
        else:
            print("Некоректный ввод")
