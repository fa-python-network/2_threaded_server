import socket
import threading

sock = socket.socket()
port = int(input('Enter the port you want a server to run on: '))

try:
    sock.bind(('localhost', port))
except:
    raise ConnectionError(f':${port} already in-use by another application')

sock.listen(1)

def handle(connection, clients, id):
    while True:
        msg = connection.recv(1024).decode()
        print(f'User {id}: {msg}\n')

        if msg == 'exit':
            clients.remove(connection)
            break
        else:
            for i in clients:
                if i != connection:
                    i.send((f'User {id}: ' + msg).encode('utf-8'))

    print(f'User {id} disconnected!')
    connection.close()

def run():
    clients = []
    id = 0

    try:
        print('Use Ctrl+C to kill the server')

        while True:
            con, _ = sock.accept()
            print(f'User ${id} connected, listening to data...')

            threading.Thread(
                target=handle, args=(
                    con, clients, id
                ), daemon=True
            ).start()
        
            clients.append(con)
            print(f'Current client count ${id}')
    except KeyboardInterrupt:
        print('Server stopped successfully.')

run()
