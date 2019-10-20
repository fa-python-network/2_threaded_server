import socket
import threading

def increment_client_port(number_port):
    return 1024 if number_port >= 65535 else number_port + 1


def check_input_host(host_address):
    try:
        if host_address == 'localhost':
            return True
        else:
            host_address_list = host_address.split('.')
            for i in host_address_list:
                if int(i) <= 0 or int(i) > 255:
                    return False
            else:
                return True
    except ValueError:
        return False


def check_input_port(port_number, default_value=9090):
    try:
        port_number = int(port_number)
        if 1024 > port_number or port_number >= 65535:
            raise ValueError
        print(f"Data is correct. Port is {port_number}")
    except ValueError:
        print(f"Data is not correct. Port is {default_value}")
        port_number = default_value
    return port_number


def receive_and_print():
    for message in iter(lambda: sock.recv(1024).decode(), ''):
        print(message)



host = input("Input host address IPv4 or localhost, DEFAULT - 127.0.0.1: ")

if check_input_host(host):
    print(f"Data is correct. Host is {host}")
else:
    print('Data is not correct. Host is 127.0.0.1')
    host = '127.0.0.1'

port = input('Input port. Default - 9090: ')
port = check_input_port(port)

client_port = input('Input port of your connection. Default: 60272. ')
client_port = check_input_port(client_port, default_value=60272)

while True:
    try:
        sock = socket.socket()
        sock.bind(('127.0.0.1', client_port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((host, port))
        break
    except OSError:
        sock.close()
        client_port += increment_client_port(client_port)

msg = ''
background_thread = threading.Thread(target=receive_and_print)
background_thread.daemon = True
background_thread.start()

while msg.lower().strip() != "exit":
    msg = input('[You]: ')
    sock.send(msg.encode())
