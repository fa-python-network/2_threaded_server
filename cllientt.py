from socket import socket


sock = socket()
host, port = input('Enter "host:port"\n').split(':')  # localhost:5050

try:
    sock.connect((host, int(port)))
except ConnectionError:
    print("Connection error")
else:
    print(f"Connection with {host}:{port} established")

    try:
        sock.send(input('Enter message to send: ').encode())
    except ConnectionError:
        print('Sending message error')
    else:
        print(f'Message sent to {host}:{port}')

        answer_blocks = []
        while True:
            answer_blocks.append(sock.recv(1024).decode())
            if not answer_blocks[-1]:
                break

        answer = ''.join(answer_blocks)
        print(f'{answer} gotten back from server')
        sock.close()

input('Press Enter to exit...')
