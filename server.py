import socket 
import threading 
import time
import csv
import sys

def port_listen():

	#Прослушивает порт, принимает запос на подкоючение от пользователя
	
	sock = socket.socket()
	sock.bind(('', 9090))
	sock.listen(1)
	while True:
		conn, addr = sock.accept()
		user_data_exchange(conn, addr)


def auth (conn, addr):

    #Функция авторизации пользователей
    arr = {}
    conn.send(("Введите Ваш логин: ").encode())
    login = conn.recv(1024).decode()

    #Чтение списка пользователей из csv файла

    with open('users.csv', 'r') as users:
        reader = csv.reader(users)
        for row in reader:
            for i in range(len(row)):
                cur_arr = row[i].split(";")
                arr[cur_arr[0]] = [cur_arr[1],cur_arr[2]]

    #Проверка пользователя, передача соответствующих сообщений 

    if login in arr.keys():
        conn.send(("Введите пароль: ").encode())
        password = conn.recv(1024).decode()
        if password == arr[str(login)][1]:
            hi_msg = "Добро пожаловать, " + str(arr[str(login)][0])
            conn.send(hi_msg.encode())

    #При отсутствии пользователя в файле, вызов функции регистрации
    else:
        reg(conn, login)



def reg(conn, login):

    #Функция регистрации пользователей        

    conn.send(("Придумайте логин: ").encode())
    name = conn.recv(1024).decode()
    conn.send(("Придумайте пароль: ").encode())
    password = conn.recv(1024).decode()
    hi_msg = "Добро пожаловать, " + name 
    conn.send(hi_msg.encode())
    new_user = [str(login), name, password]
    with open('users.csv', 'w', newline='') as users:
        writer = csv.writer(users, delimiter = ';')
        writer.writerow(new_user)


def user_data_exchange(conn, addr):

	auth(conn, addr)
	while True:
		print('here')
		data = conn.recv(1024)
		if not data:
			break
		msg = data.decode()
		print(msg)


if __name__ == "__main__":
    port_listen()

