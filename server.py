import socket
import threading

def client(conn, addr):
    print('Запустился новый поток')
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
        print(f'Порт занят {port}')
        port += 1

print (f'Сервер подключился к порту: {port}')
sock.listen(3)

while True:
    conn, addr = sock.accept()
    print(f'Клиент {addr} подключился к серверу')
    p = threading.Thread(target = client, args = (conn, addr))
    p.start()

sock.close()
print('Сервер завершил работу')
