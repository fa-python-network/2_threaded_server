import socket
from datetime import datetime
import threading
import json


def output_service(txt):
    """" Здесь выводятся служебные сообщения в консоль и в log-файлы! """
    try:
        with open('log.txt', 'r') as f:
            data = f.read()

        data += f'[{str(datetime.today())[:10]}] [{str(datetime.today())[11:-10]}] {txt}\n'

        with open('log.txt', 'w') as f:
            f.write(data)

        print(txt)
    except FileNotFoundError:
        with open('log.txt', 'a') as f:
            pass
        output_service(txt)


def read_data():
    """ Читаем логины, пароли """
    with open('data.json', "r") as f:
        data = json.load(f)
    return data


def write_data(data):
    """ Записываем в базу зареганных пользователей """
    with open('data.json', "w") as f:
        json.dump(data, f)


def choice_user(conn):
    """ Предлгаем пользователю пройти аутификацию """
    try:
        conn.send('\n1 - Log in\n2 - Sign up\n\n0 - Close program\n'.encode())
        choice = conn.recv(1024).decode()
        if choice == '1':
            login(conn)
        elif choice == '2':
            registration(conn)
            login(conn, txt_error='User successfully registered! Log in!')
        elif choice == '0':
            conn.send("You are disconnected from the server!\n".encode())
            conn.close()
        else:
            choice_user(conn)
    except ConnectionResetError:
        # Если вдруг пользователь нажмёт крестик на данном этапе программы
        pass


def login(conn, txt_error=None):
    """ Даём пользователю зайти """
    global login_inp

    try:
        if txt_error == None:
            conn.send(f'Login ↓ '.encode())
        else:
            conn.send(f'\n{txt_error}\nLogin ↓ '.encode())

        login_inp = conn.recv(1024).decode()
        data = read_data()
        try:
            data[login_inp]   # проверка, присутствиует ли логин в базе
            conn.send('Password ↓ '.encode())
            password_inp = conn.recv(1024).decode()

            if password_inp == data[login_inp]["password"]:
                # Отправляем пользователю информацию о пользователях онлайн
                online_lst = 'You, '
                count = 1
                for i in users_online:
                    count += 1
                    online_lst += f'{users_online[i]}, '
                online_lst = f'Total Online: {count}\nOf them: {online_lst[:-2]}'

                conn.send(f'\n{data[login_inp]["nickname"]}, successfully logged in! '
                          f'You are added to the chat, you can write\n{online_lst}\n'.encode())
                txt = f'User %{data[login_inp]["nickname"]}% successfully logged in!'
                output_service(txt)
            else:
                login(conn, txt_error='Wrong password!')
        except KeyError:
            login(conn, txt_error='Wrong login!')
    except ConnectionResetError:
        # Если вдруг пользователь нажмёт крестик на данном этапе программы
        pass


def registration(conn, txt=None):
    """ Регестрируем пользователей """
    try:
        data = read_data()
        if txt == None:
            conn.send("Enter login ↓ ".encode())
        else:
            conn.send(f"\n{txt}\nEnter password ↓ ".encode())
        login = conn.recv(1024).decode()
        if login in data:
            registration(conn, txt="A user with this login already exists!")
        else:
            conn.send('Enter password ↓ '.encode())
            password = conn.recv(1024).decode()

            conn.send('Username ↓ '.encode())
            nick = conn.recv(1024).decode()

            data[login] = {'password': password, 'nickname': nick}
            write_data(data)

            txt = f'New user registered %{data[login_inp]["nickname"]}%'
            output_service(txt)

    except ConnectionResetError:
        # Если вдруг пользователь нажмёт крестик на данном этапе программы
        pass


def Choose_port():
    """  Выбор порта """
    try:
        choose_port = input('Port / Press "Enter" for default value > ')
        if choose_port == '':
            choose_port = 9090
        else:
            choose_port = int(choose_port)
        return choose_port
    except ValueError:
        print('Need integer value!')
        Choose_port()


def start_server(port):
    """   Пытаемся подключиться к выбранному порту, если не получается, то берем следующий и т.д,
    пока не подключимся   """
    try:
        sock.bind(('', port))
        output_service('Server is running!')
        txt = f'Server is listening on port {port}'
        output_service(txt)

        isWorking = True
        start(isWorking)
    except OSError:
        port += 1
        start_server(port)
    except OverflowError:
        # На случай, если порт был введен не диапозоне портов
        port = 9090
        start_server(port)


def start(isWorking=None):
    """   Сервер слушает и отправляет пользователей в разные потоки   """
    sock.listen(1)
    conn, addr = sock.accept()

    t = threading.Thread(target=reader, args=(conn, addr, isWorking))
    t.start()

    start(isWorking=True)


def reader(conn, addr, isWorking):
    """ Работа с конкретным пользователем """
    global users_online

    try:
        choice_user(conn)

        user_data = read_data()
        users_online[conn] = user_data[login_inp]["nickname"]

        for i in users_online:
            if i == conn:
                pass
            else:
                i.send(f'*{users_online[conn]} connected to chat*'.encode())
        txt = f'User %{users_online[conn]}% connected to chat'
        output_service(txt)

        while isWorking:
            data = conn.recv(1024)
            msg = data.decode()

            if msg == '/exit':
                for i in users_online:
                    if i == conn:
                        i.send('You were disconnected!\n'.encode())
                    else:
                        i.send(f'*{users_online[conn]} disconnected from the chat*'.encode())
                txt = f'User %{users_online[conn]}% disconnected from the chat'
                output_service(txt)
                del users_online[conn]
                conn.close()
            else:
                for i in users_online:
                    if i == conn:
                        pass
                    else:
                        i.send(f'[{str(datetime.today())[11:-10]}] {users_online[conn]} > {msg}'.encode())

                txt = f'{users_online[conn]} > {msg}'
                output_service(txt)
    except ConnectionResetError:
        # На случай, если пользователь не умеет писать /exit и жмякает крестик
        for i in users_online:
            if i == conn:
                pass
            else:
                i.send(f'*{users_online[conn]} disconnected from the chat*'.encode())
        txt = f'User %{users_online[conn]}% disconnected from the chat'
        output_service(txt)
        del users_online[conn]
        conn.close()
    except OSError:
        # если вдруг попытаемся сделать что-то с уже отключенным пользователем
        pass
    except NameError:
        # Если вдруг пользователь уже отключился на этапе аутификации
        pass


users_online = {}
sock = socket.socket()
port = Choose_port()

start_server(port)
