import socket
from datetime import datetime
import threading


def start_server(port):
    try:
        sock.bind(('', port))
        print('Server is running!')
        isWorking = True
        start(isWorking)
    except OSError:
        port += 1
        start_server(port)


def Choose_port():
    try:
        choose_port = input('Port > ')
        if choose_port == '':
            choose_port = 9090
        else:
            choose_port = int(choose_port)
            print(type(choose_port))
        return choose_port
    except ValueError:
        print('Need integer value!')
        Choose_port()


def start(isWorking=None):
    print(f'Server is listening on port {port}')
    sock.listen(1)
    conn, addr = sock.accept()

    t = threading.Thread(target=reader, args=(conn, addr, isWorking))
    t.start()

    start(isWorking=True)


def reader(conn, addr, isWorking):
    try:
        while isWorking:
            data = conn.recv(1024)
            msg = data.decode()

            if msg == '/exit':
                conn.send('You were disconnected!\n'.encode())
                conn.close()
                isWorking = False
                start(isWorking=True)

            else:
                print(f'Address = {addr[0]}\n'
                      f'Date: {str(datetime.today())[:10]}\n'
                      f'Time: {str(datetime.today())[11:-7]}\n'
                      f'Message: {msg}\n')

                response = 'Message delivered!\n'
                conn.send(response.encode())
    except ConnectionResetError:
        pass


sock = socket.socket()
port = Choose_port()

start_server(port)
