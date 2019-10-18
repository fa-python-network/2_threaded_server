import csv
import socket
from hashlib import sha256
import threading
import logging as log


class User(threading.Thread):
    def __init__(self, conn, addr):
        super(User, self).__init__()
        self.conn = conn
        self.addr = addr
        self.login = self.aunt()

    def send_msg_all_user(self, msg):
        with lock_msg:
            logger_msg.info(f'{self.login}: {msg}')
            for user in pool:
                if self.login != user.login:
                    user.conn.send(f'{user.login}: {msg}'.encode())

    def aunt(self): #choose sign in or sign up
        self.conn.send('Have you alredy had your own acc?(y/n) '.encode())
        event = ''.join(conn.recv(1024).decode().split()) # delete wrong space
        if event.upper() in ['1', 'Y', 'YES', 'HAVE', 'Н']:
            return self.enter()
        else:
            return self.create_acc()

    def enter(self): #enter to account
        self.conn.send("Enter the login: ".encode())
        login = self.conn.recv(1024).decode()
        self.conn.send("Enter the password: ".encode())
        password = sha256(self.conn.recv(1024)).hexdigest()

        file = 'passwords.csv'
        with lock:
            with open(file, 'r') as f:
                read = csv.DictReader(f, delimiter=' ')
                for line in read:
                    if line['login'].upper() == login.upper() and line['password'].upper() == password.upper():
                        self.conn.send("Welcome {} to the server".format(login).encode())
                        return login

            self.conn.send('Wrong login or password \nDo you want to restart enter (y/n)? '.encode())
            event = ''.join(conn.recv(1024).decode().split())

            if event.upper() in ['Y', 'YES', 'AGREE', 'DA', '']:
                self.aunt()

    def create_acc(self): #create_account
        self.conn.send("Enter the new login: ".encode())
        login = self.conn.recv(1024).decode()
        self.conn.send("Enter the new password: ".encode())
        password = sha256(self.conn.recv(1024)).hexdigest()
        login = ''.join(login.split())
        file = 'passwords.csv'
        with lock:
            with open(file, 'a') as f:
                f.write(login + ' ' + password + '\n')

        return self.enter()

    def run(self):
        while True:
            msg = self.conn.recv(1024).decode()
            print(f"{self.login}: {msg} ")
            self.send_msg_all_user(msg)



sock = socket.socket()
maxclients = 5
port = int(input("Enter the port: "))
lock = threading.Lock()
lock_msg = threading.Lock()


while True:
    try:
        sock.bind(("",port))
        break
    except:
        port += 1
        if port > 65535:
            print("Not founded the port")
            exit(0)

pool = []
sock.listen(maxclients)
logger_msg = log.getLogger("logger_msg")
logger_msg_handler = log.FileHandler(filename='logger_msg_file.log', encoding='UTF-8')
logger_msg_handler.setLevel(log.INFO)
logger_msg.addHandler(logger_msg_handler)
logger_msg.setLevel(log.INFO)
while True:
    conn, addr = sock.accept()
    user = User(conn, addr)
    pool.append(user)
    user.start()









