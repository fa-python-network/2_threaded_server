import socket
import json
import threading


def read_data():
    with open('data.json', "r") as f:
        data = json.load(f)
    return data


def write_data(data):
    with open('data.json', "w") as f:
        json.dump(data, f)


def login():
    global login_inp
    login_inp = input('Login > ')
    data = read_data()

    try:
        data[login_inp]

        password_inp = input('Password > ')
        if password_inp == data[login_inp]["password"]:
            print(f'{data[login_inp]["nickname"]}, успешно выполнен вход!')
            connect_to_server()
        else:
            print('Неверный пароль!')
            login()
    except KeyError:
        print('Такого логина нет!')
        login()


def registration():
    data = read_data()
    ur_login = input("Введите логин > ")
    if ur_login in data:
        print("Пользователь с таким логином уже существует!")
        registration()
    ur_password = input('Введите пароль > ')
    ur_nick = input('Имя пользователя > ')

    data[ur_login] = {'password': ur_password, 'nickname': ur_nick}
    write_data(data)

    print('Пользователь успешно добавлен в базу данных!\nАвторизуйтесь!')
    login()


def ur_choice():
    choice = input('1 - Авторизоваться\n'
                   '2 - Зарегистрироваться\n\n'
                   '0 - Закрыть программу\n')
    if choice == '1':
        login()
    elif choice == '2':
        registration()
    elif choice == '0':
        print('Работа программы успешно завершена!')
    else:
        ur_choice()


def Choose_hostname():
    choose_hostname = input('Host name > ')
    if choose_hostname == '':
        choose_hostname = 'localhost'
    return choose_hostname


def Choose_port():
    try:
        choose_port = input('Port > ')
        if choose_port == '':
            choose_port = 9090
        else:
            choose_port = int(choose_port)
        return choose_port
    except ValueError:
        print('Need integer value!')
        Choose_port()


def connect_to_server():
    sock = socket.socket()
    hostname = Choose_hostname()
    port = Choose_port()

    try:
        sock.connect((hostname, port))
        print(f'Connected to host: {hostname}\n{" "* 13}port: {port}')

        isWorking_local = True
        t2 = threading.Thread(target=working, args=(sock, isWorking_local))
        t2.start()

        # t = threading.Thread(target=listen, args=(sock,))
        # t.start()

        #working()
    except:
        print('Incorrect hostname or port')
        connect_to_server()


def working(sock, isWorking=None):
    while isWorking:
        msg = input('Message > ')
        if msg.lower() == '/exit':
            isWorking = False
        else:
            sock.send(msg.encode())
            msg_from_server = sock.recv(1024)
            msg = msg_from_server.decode()
            print(msg)

    sock.close()


def listen(sock):
    msg_from_server = sock.recv(1024)
    msg = msg_from_server.decode()
    print(msg)


ur_choice()
