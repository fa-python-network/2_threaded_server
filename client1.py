from socket import socket


sock = socket()

try:
    sock.connect(('localhost', 8888))
except ConnectionError:
    print("Server is not available")
else:
    print("Connected to server")

    try:
        sock.send(input('Enter message to server: ').encode())
    except ConnectionError:
        print('Error while sending data')
    else:
        print('Message sent')

        answer = b''
        while True:
            chunk = sock.recv(1024)
            answer += chunk
            if not chunk:
                break

        print(f'Received from server: {answer.decode()}')
        sock.close()

input('Press Enter to exit...')
