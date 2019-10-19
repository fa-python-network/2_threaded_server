import socket 
from threading import Thread
import time
import csv
import sys

def receiver(conn):
    try:
        answ = conn.recv(16384).decode()
        return answ
    except:
        print("Пользователь отключился")
        conn.close()
    
def sender(conn, msg):
    try:
        conn.send(msg.encode())
    except:
        print("Пользователь отключился")
        conn.close()


def port_listen():

	#Прослушивает порт, принимает запос на подключение от пользователя
	
    while True:
        sock = socket.socket()
        sock.bind(('', 9090))
        sock.listen(1)

        try:
            while True:
                conn, addr = sock.accept()
                Thread(target = user_data_exchange, args = (conn, addr)).start()

        finally:
            sock.close()
"""
    	while True:
    		conn, addr = sock.accept()
    		user_data_exchange(conn)

"""

def auth (conn):

    #Функция авторизации пользователей
    arr = {}
    sender(conn, "Введите Ваш логин: ")
    login = receiver(conn)

    #Чтение списка пользователей из csv файла

    with open('users.csv', 'r') as users:
        reader = csv.reader(users)
        for row in reader:
            for i in range(len(row)):
                cur_arr = row[i].split(";")
                arr[cur_arr[0]] = [cur_arr[1]]
        users.close()

    #Проверка пароля

    auth_status = False
    while auth_status != True:
        if login in arr.keys():
            sender(conn, "Введите пароль: ")
            password = receiver(conn)
            if password == arr[str(login)][0]:
                hi_msg = "Добро пожаловать, " + str(login)
                sender(conn, hi_msg)
                auth_status = True
                chat(conn)
            else:
                sender(conn, "Неверный пароль!")
                
        #При отсутствии пользователя в файле, отправка соответствующего сообщения, повторный запрос действия
        else:
            sender(conn, "Пользователь не найден \n")
            user_data_exchange(conn)
            break



def reg(conn):

    #Функция регистрации пользователей        

    sender(conn, "Придумайте логин: ")
    login = receiver(conn)
    arr = {}

    with open('users.csv', 'r') as users:
        reader = csv.reader(users)
        for row in reader:
            for i in range(len(row)):
                cur_arr = row[i].split(";")
                arr[cur_arr[0]] = [cur_arr[1]]
        users.close()

    if (login in arr.keys()):
        sender(conn, "Логин занят!")
        reg(conn)
    else:    
        sender(conn, "Придумайте пароль: ")
        password = receiver(conn)
        hi_msg = "Добро пожаловать, " + login 
        sender(conn, hi_msg)
        new_user = [login, password]
        with open('users.csv', 'a', newline='') as users:
            writer = csv.writer(users, delimiter = ';')
            writer.writerow(new_user)
        chat(conn)


def user_data_exchange(conn, addr):

    sender(conn, "Для входа введите 1, для регистрации введите 2: ")
    answ = receiver(conn)

    user_check = False
    while(user_check != True):

        if answ == '1':
            user_check = True    
            auth(conn)
        elif answ == '2':
            user_check = True
            reg(conn)
        elif type(conn) == socket:
            conn.send(("Для входа введите 1, для регистрации введите 2: ").encode())
            answ = receiver(conn)
        else:
            break

def chat(conn):

    while True:
        print("Hello")
        break

if __name__ == "__main__":
    port_listen()

