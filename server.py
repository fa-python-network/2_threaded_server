import socket
import threading

def client(conn, addr):
    print('New thread')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode())
        conn.send(data)
    

sock = socket.socket()
port = 9090

while True:
    try:
        sock.bind(('', port))
        break
    except:
        print(f'Port {port} is busy')
        port += 1

print (f'Server connected to port: {port}')
sock.listen(3)

while True:
    conn, addr = sock.accept()
    print(f'Client {addr} connected to server')
    p = threading.Thread(target = client, args = (conn, addr))
    p.start()

sock.close()
print('Server is over')