import socket
import sys
import threading
import json
import logging


class Server():
    def __init__(self, clients=[]):
        self.clients=clients
        self.port=int(input("Введите номер порта: "))
        self.sock=None
        self.users=self.load_users()
        self.start_server()

    @staticmethod
    def load_users():
        """
        функция загрузки пользователей из файла users.json
        """
        with open('users.json', 'r') as f:
            user_dict=dict(json.load(f))
        return user_dict

    def save_user(self):
        """
        функция записи пользователей в файл users.json
        """
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    def start_server(self):
        self.sock=socket.socket()
        while True:
            try:
                self.sock.bind(('',self.port))
                break
            except:
                self.port+=1
        print(f'Выбран порт {self.port}')
        self.sock.listen(6)
        while True:
            conn,addr=self.sock.accept()
            print(f"Присоединился клиент с ip {addr}")
            threading.Thread(target=self.client,args=(conn,addr)).start()
            self.clients.append([conn, addr])
    

    def send_to_all_clients(self,from_addr, msg):
        """
        функция отправки сообещний всем пользователям чата
        """
        for i in self.clients:
            if i[1] != from_addr:
                i[0].send(msg.encode())
                


    def client(self,conn,addr):
        conn.send('Введите ваше имя: '.encode())
        name_user = conn.recv(1024).decode()
        if name_user in self.users:
            conn.send('Введите пароль: '.encode())
            password = conn.recv(1024).decode()
            if password == self.users[name_user]['password']:
                conn.send(f'Добро пожаловать {name_user}'.encode())
            else:
                while True:
                    conn.send('Неверный пароль, повторите ввод пароля: '.encode())
                    password = conn.recv(1024).decode()
                    if password == self.users[name_user]['password']:
                        conn.send(f'Добро пожаловать {name_user}'.encode())
                        break

        else:
            conn.send(f"Пользователя {name_user} не существует\n Зарегистрироваться?(y/n)".encode())
            answer = conn.recv(1024).decode()
            if answer == 'y':
                conn.send('Введите имя повторно: '.encode())
                new_name_user = conn.recv(1024).decode()
                while new_name_user in self.users:
                    conn.send('Это имя занято, придумайте новое: '.encode())
                    new_name_user = conn.recv(1024).decode()
                conn.send('Введите пароль, минимум 3 символа: '.encode())
                new_password = conn.recv(1024).decode()
                while len(new_password) < 3:
                    conn.send('Пароль должен быть от 3 символов: '.encode())
                    new_password = conn.recv(1024).decode()
                self.users[new_name_user] = {"password":new_password}
                with lock_for_file:
                    self.save_user()
                conn.send(f'{new_name_user}, вы успешно зарегистрированы'.encode())
                name_user = new_name_user
            else:
                conn.send('До свидания, это ваш выбор'. encode())
                conn.close()


            
        while True:
            try:
                data=conn.recv(1024).decode()
                if not data:
                    conn.close()
                    break
                else:
                    serv_log.info(f"{name_user}:{data}") #запись сообешний в лог файл
                    with lock_for_msg:
                        self.send_to_all_clients(addr, f"{name_user}:{data}")
            except (ConnectionError, OSError):
                print(f"Клиент {name_user}, отключился")
                try:
                    for i in range(len(self.clients)):
                        if self.clients[i][1] == addr:
                            self.clients.pop(i)
                except:
                    pass
                break
#создание логгера
serv_log = logging.getLogger('log_')
serv_log_handler = logging.FileHandler('messages.log', encoding = 'UTF-8')
serv_log_handler.setLevel(logging.INFO)
serv_log.addHandler(serv_log_handler)
serv_log.setLevel(logging.INFO)

lock_for_file = threading.Lock()
lock_for_msg = threading.Lock()

serv_=Server()
