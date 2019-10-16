import socket

def send_msg(sock, msg):
    header = f'{len(msg):<4}'
    sock.send(f'{header}{msg}'.encode())


def recv_msg(sock):
    header = int(sock.recv(4).decode().strip())
    data = sock.recv(header*2).decode()
    return data


from time import sleep
sock = socket.socket()
k = False
while not k:
    try:
        print("Host:")
        host = input()
        if host == "":
            host = 'localhost'
        print("Port:")
        port = input()
        if port == "":
            port = 9090

        sock.connect((host, int(port)))
        #print(f"Если вы новый пользователь, введите 1 \n Если хоти войти, введите 2")
        #login = input()
        #while login != 1 or login != 2:
            #print("Неверное значение")
            #login = input()

         # регистрация нового пользователя
        #if login == 1:
            #print("Введите свое Имя")
            #msg = input()
            #send_msg(sock, msg)
            #цршду


        #c = recv_msg(sock)
        # создаем нового пользователя, если его нет в файле
        #if c == "What is your name?":
            #print("Введите свое Имя")
            #msg = input()
            #send_msg(sock, msg)
            #print("введите пароль")
            #psw = input()
            #send_msg(sock, psw)
            #c = recv_msg(sock)

        #c1 = recv_msg(sock)
        #print("Введите пароль")
        #psw = input()
        #while c1 != psw:
            #print(f"Неверный пароль \n Введите пароль")
            #psw = input()


        print("Введите сообщение")
        print("Для выхода введите exit")
        msg = input()
        while msg != 'exit':
            send_msg(sock, msg)
            data = recv_msg(sock)
            print(data)
            msg = input()
        k = True
    except KeyboardInterrupt:
        break
sock.close()