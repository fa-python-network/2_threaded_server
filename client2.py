import socket
import threading


def Choose_hostname():
    choose_hostname = input('Host name / Press "Enter" for default value > ')
    if choose_hostname == '':
        choose_hostname = 'localhost'
    return choose_hostname


def Choose_port():
    choose_port = input('Port / Press "Enter" for default value > ')
    if choose_port == '':
        choose_port = 9090
    return choose_port


def connect_to_server():
    hostname = Choose_hostname()
    port = int(Choose_port())
    try:
        sock.connect((hostname, port))
        print(f'Connected to host: {hostname}\n{" "* 13}port: {port}')
        # Авторизация
        while True:
                msg = sock.recv(1024).decode()
                print(msg)
                if 'successfully logged in!' in msg:
                    break
                response = input()
                sock.send(response.encode())

        t = threading.Thread(target=listen, args=(sock,))
        t.setDaemon(True) 
        t.start()
        
        isWorking = True
        while isWorking:
            msg = input()
            if msg.lower() == '/exit':
                sock.send(msg.encode())
                isWorking = False
            else:
                sock.send(msg.encode())
        print('Closed')
        sock.close()

    except ValueError:
        print('Port must be integer value!')
        connect_to_server()

    except TypeError:
        print('Port must be integer value!')
        connect_to_server()

    except socket.gaierror:
        print('Incorrect host')
        connect_to_server()

    except ConnectionRefusedError:
        # На случай, если введен не верный адрес и подключение невозможно
        print('Incorrect address! Try again!')
        connect_to_server()


def listen(sock):
    while True:
        msg = sock.recv(1024).decode()
        print(msg)


sock = socket.socket()
connect_to_server()
