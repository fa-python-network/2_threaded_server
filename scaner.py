import socket
import threading

def scan(name):
    pass

scan = socket.socket()
num_port = 1
host_name = input("Любезнейший, прошу вас, введите имя хоста ")

while num_port != 65536:
    try:
        scan = socket.socket()
        scan.connect((host_name,num_port))
        print(f"Порт {num_port} открыт")

    except OSError:
        pass
        # print(f"Порт {num_port} закрыт")
    finally:
        num_port += 1
        scan.close()



