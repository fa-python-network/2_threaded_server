import socket


class Client(socket.socket):
    """Клиент"""

    def __init__(self):
        """я задоллбался писать эти комментарии и так вроде всё понятно"""
        super().__init__()
        self.sock = socket.socket()

    def send_msg(self, msg, sock):
        length_msg = str(len(msg))
        length_msg = '0' * (10 - len(length_msg)) + length_msg
        msg = length_msg + msg
        sock.send(msg.encode())

    def recv_msg(self, sock):
        length_msg = int(sock.recv(10).decode())
        msg = sock.recv(length_msg).decode()
        return msg

    def new_user(self, sock):
        print("Введите ваше имя: ")
        name = input()
        self.send_msg(name, sock)
        while True:
            print("Введите пароль")
            password = input()
            print("Повторите пароль")
            password2 = input()
            if password == password2:
                break
        self.send_msg(password, sock)

    # Это не безопасно, но мне лень делать что-то другое, ибо я тупенький)
    def old_user(self, sock, msg):
        print(msg)
        password = input()
        self.send_msg(password, sock)
        flag = self.recv_msg(sock)
        if flag == "0":
            self.send_msg('1', sock)
            return
        else:
            self.old_user(sock, 'Введите правильный пароль')

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

    def hi(self):
        # Получение приветствия или просьбы зарегестрироваться
        data = self.recv_msg(self.sock)
        if int(data):
            self.new_user(self.sock)
        else:
            self.old_user(self.sock, 'Введите пароль:')
        data = self.recv_msg(self.sock)
        print(data)

    def chatting(self):
        print('Для окончания работы с сервером введите exit ')
        msg = input()

        while msg != 'exit':
            self.send_msg(msg, self.sock)

            data = self.recv_msg(self.sock)
            print(data)

            msg = input()

        self.end()

    def end(self):
        self.sock.close()
        print('Разрыв соединения с сервером')

    def run(self):
        self.connection()
        self.hi()
        self.chatting()


sock = Client()
sock.run()
