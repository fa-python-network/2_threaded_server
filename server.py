import socket
import logging
import json
import hashlib
import threading
import time


class UserThread(threading.Thread):
    def __init__(self, conn, addr, user_thread_id):
        super(UserThread, self).__init__()
        self.conn = conn
        self.addr = addr
        self.user_thread_id = user_thread_id

        # На тот случай, если пользователь не залогинился,
        # но будет вызвана функция get_login
        self.login = None
        # ===============
        self.login = self.sign_in()

    def run(self) -> None:
        """
        Основная работа по получению сообщений от пользователя
        :return: None
        """
        # TODO добавить команды для пользователей (в т.ч. узнать текущий онлайн)
        while True:
            try:
                msg = ''
                data = self.conn.recv(1024)
            except ConnectionError:
                server_logger.info(f"[{self.login}{self.addr}] разорвал соединение")
                break
            if not data:
                break
            msg += data.decode()
            users_messages_logger.info(f"[{time.time()}][{self.login}{self.addr}] прислал сообщение: {msg}")
            with send_lock:
                send_to_all("["+self.login+"]: " + msg, self.addr)

        conn.close()
        server_logger.info(f"[{self.login}{self.addr}] отключился")

    def sign_in(self) -> str:
        """
        Для осуществления входа пользователя
        или его регистрации, если такого пользователя нету
        :return: login -> str
        """
        while True:
            self.conn.send("Введите логин: ".encode())
            login = self.conn.recv(512).decode()
            if login in users:
                while True:
                    conn.send("Введите пароль: ".encode())
                    password = hashlib.md5(conn.recv(1024)).hexdigest()
                    if password == users[login]:
                        server_logger.info(f"Клиент [{login}]{self.addr} вошел")
                        break
            else:
                while True:
                    conn.send("Введите логин для регистрации: ".encode())
                    login = conn.recv(1024).decode()
                    if login not in users:
                        break
                conn.send("Введите пароль".encode())
                password = hashlib.md5(conn.recv(1024)).hexdigest()
                users[login] = password
                server_logger.info(f"Клиент [{login}]{self.addr} зарегистрировался")
                with lock:
                    with open("users.json", "w") as f:
                        json.dump(users, f)
            conn.send(f"{login}, поздаровайтесь с чатом\nОнлайн сейчас: {threading.active_count() - 1}".encode())
            return login

    def get_login(self) -> str:
        """
        Возвращает логин пользователя из потока
        :return: login -> str
        """
        return self.login


# Блокировка для регистрации нового пользователя (т.к. осуществляет доступ к файлу)
lock = threading.Lock()

# Блокировка для отправки сообщения всем пользователям (что connection не сломался =))
send_lock = threading.Lock()

# Заранее получаем пользователей, чтобы потом не терять на этом время
with open("users.json", "r") as users_file:
    users = dict(json.load(users_file))


# ================= Logger for server ========================================
server_logger = logging.getLogger("server_logger")
log_handler = logging.FileHandler(filename="server_log.log", encoding="UTF-8")
log_handler.setLevel(logging.INFO)
server_logger.addHandler(log_handler)
server_logger.setLevel(logging.INFO)
# ===========================================================================

# ================= Logger for users messages ======================================
users_messages_logger = logging.getLogger("users_logger")
log_handler_msg = logging.FileHandler(filename="messages_log.log", encoding="UTF-8")
log_handler_msg.setLevel(logging.INFO)
users_messages_logger.addHandler(log_handler_msg)
users_messages_logger.setLevel(logging.INFO)
# ==================================================================================

sock = socket.socket()
default_port = 9090

# Цикл поднятия сервера =\
while True:
    try:
        port = int(input("Введите порт на котором хотите меня поднять: "))
        if port > 65535 or port < 0:
            print("Порт должен быть числом в диапазоне 0-65535")
        else:
            break
    except TypeError:
        print("Порт должен быть числом в диапазоне 0-65535")

try:
    sock.bind(('', port))
except ConnectionError:
    print("Похоже, к этому порту нельзя причалиться =( пробую поискать другой . . .")
    try:
        for i in range(8080, 65535):
            print(f"Пробуем забиндить порт {i}")
            sock.bind(('', i))
            break
    except ConnectionError:
        print("Занято...")

sock.listen(100)

server_logger.info("Сервер поднят!")


def send_to_all(msg, addr) -> None:
    """
    Идём в цикле по "живым" пользователям и отправляем им сообщение

    :param msg: Сообщение от пользователя addr
    :param addr: IP и PORT пользователя, который отправил сообщение
    :return: None
    """
    for i in users_threads:
        if i.is_alive():
            if i.get_login() is not None and i.addr != addr:
                i.conn.send(msg.encode())
                print(f"Отправлено к {i.addr} от {addr}")


def server_cmd() -> None:
    while True:
        cmd = input("Введите команду: ")
        if cmd == "stop":
            # Unbelievable
            exit(0)
        elif cmd == "show ml":
            with open("messages_log.log", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    print(line)
        elif cmd == "show sl":
            with open("server_log.log", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    print(line)


# ======= Thread for server commands ============
main_thread = threading.Thread(target=server_cmd)
main_thread.start()
# ===============================================

users_threads = []
while True:
    conn, addr = sock.accept()
    server_logger.info(f"{addr} подключился к серверу!")
    a = UserThread(conn, addr, len(users_threads))
    a.start()
    users_threads.append(a)
