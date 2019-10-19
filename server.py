import socket 
import threading 
import time
import csv
import sys

def port_listen():
	"""
	Прослушивает порт, соединяется с пользователем
	"""

	sock = socket.socket()
	sock.bind(('', 9090))
	sock.listen(1)
	while True:
		conn, addr = sock.accept()
		user_data_exchange(conn, addr)



#Функция авторизации пользователей
def auth (conn, addr):

    ip = addr[0]
    arr = {}

    #Чтение списка пользователей из csv файла
    with open('users.csv', 'r') as users:
        reader = csv.reader(users)
        for row in reader:
            for i in range(len(row)):
                cur_arr = row[i].split(";")
                arr[cur_arr[0]] = [cur_arr[1],cur_arr[2]]

    #Проверка пользователя, передача соответствующих сообщений 
    if str(ip) in arr.keys():
        conn.send(("Введите пароль: ").encode())
        password = conn.recv(1024).decode()
        if password == arr[str(ip)][1]:
            hi_msg = "Добро пожаловать, " + str(arr[str(ip)][0])
            conn.send(hi_msg.encode())

    #При отсутствии пользователя в файле, вызов функции регистрации
    else:
        reg(conn, ip)

#Функция регистрации пользователей        
def reg(conn, ip):

    conn.send(("Введите Ваше имя: ").encode())
    name = conn.recv(1024).decode()
    conn.send(("Придумайте пароль: ").encode())
    password = conn.recv(1024).decode()
    hi_msg = "Добро пожаловать, " + name 
    conn.send(hi_msg.encode())
    new_user = [str(ip), name, password]
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

