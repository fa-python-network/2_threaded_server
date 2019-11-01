from socket import socket
from threading import Thread


def main():
    def new_client(conn, addr):
        data = ''
        while True:
            chunk = conn.recv(1024).decode()
            data += chunk
            if len(chunk) < 1024:
                break

        print(f'Sever received "{data}" from {addr}')

        conn.send(data.encode())
        print(f'{data.encode()} sent back to client')

        conn.close()
        print(f'{addr} disconnected')

    while True:
        conn, addr = sock.accept()
        addr = addr[0]
        print(f'Connected to "{addr}"')

        Thread(target=new_client, args=(conn, addr)).start()


with socket() as sock:
    sock.bind(('', 8888))
    print('Server started here')

    sock.listen(8)
    print('Port listening started')

    main()

print('"main" finished')
