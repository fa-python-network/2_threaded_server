import socket
import threading

def new_sock(port, host, ports_list):
    sock = socket.socket()
    try:
        sock.connect((host, port))
        ports_list.append(port)
        #print(f"Порт {port} свободен")
    except OSError:
        pass
        #print(f"Порт {port} занят")
    sock.close()


print("Host:")
host = input()
ports_list = []
if host == "":
    host = 'localhost'

for i in range(1, 65536):
    threading.Thread(target=new_sock, args=[i, host, ports_list]).start()
print("Список свободных портов")
#не хотелось делать отдельный цикл на вывод
print(sorted(ports_list))