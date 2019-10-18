import socket
import threading

def serve_client(conn, addr) -> None:
    msg = ''
    
    while True:
        data = conn.recv(1024)

        if not data:
            break

        msg += data.decode()
        conn.send(data)

    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', 7777))
    s.listen(100)

    while True:
        conn, addr = s.accept()
        p1 = threading.Thread(target=serve_client, args=(conn, addr))
        p1.start()

