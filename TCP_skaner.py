import socket
import threading
import os

def new_sock(port, host, ports_list):
    sock = socket.socket()
    global bar
    try:
        sock.connect((host, port))
        ports_list.append(port)
        # print(f"Порт {port} свободен")
    except OSError:
        pass
        # print(f"Порт {port} занят")
    for i in range(10):
        if bar[i] == port:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{(i+1)*10}|{'*'*(i+1)}")
            break
    sock.close()


print("Host:")
host = input()
ports_list = []
if host == "":
    host = 'localhost'
bar = [int(65535*(i/10)) for i in range(1,11)]
thread = []
for i in range(1, 65536):
    thread.append(threading.Thread(target=new_sock, args=[i, host, ports_list]))

for t in thread:
    t.start()
for t in thread:
    t.join()
print("Список свободных портов")
# не хотелось делать отдельный цикл на вывод
print(sorted(ports_list))
