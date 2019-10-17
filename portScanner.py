import socket
import sys
import threading

opened_ports = []
loader = -1

def check_port(ip, port):
    global loader
    sock = socket.socket()
    try:
        sock.connect((ip, port))
        opened_ports.append(port)
    except (ConnectionError, OSError):
        pass
    sys.stdout.write(f"\r{loader}/65535")
    loader += 1
    sock.close()


cli_ip = input("Введите ip для сканирования портов: ")
for i in range(0, 65536):
    a = threading.Thread(target=check_port, args=(cli_ip, i))
    a.start()

while threading.active_count() > 1:
    sys.stdout.write(f"\r{loader}/65535")
    pass

print("\n" + str(opened_ports))
