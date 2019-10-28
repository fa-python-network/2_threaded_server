import socket
import threading

def client(conn, addr):
    print('A new thread has launched')
    while True:
        data = conn.recv(1024)
        if not data:
            break

        print(data.decode())
        conn.send(data)

sock = socket.socket()

port = 9089

while True:
    try:

        sock.bind(('', port))
        break

    except:
        print(f'The port is busy {port}')

        port += 1

print (f'Server joined the port: {port}')

sock.listen(3)

while True:
    conn, addr = sock.accept()

    print(f'Client {addr} has joined the server')

    p = threading.Thread(target = client, args = (conn, addr))

    p.start()

sock.close()
print('Server has shut down')