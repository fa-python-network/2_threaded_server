import threading
import socket

HOST = 'localhost'
free_port = []
START = 0
END = 65535
HOWMUCH = 3000
PROCENT_LOAD = int((END - START)/100)
all_port = [i for i in range(START, END)]
procent = 0
loading = ""


def port_connect(adr, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if conn.connect_ex((HOST, port)):
        return port
    else:
        return False


def port_thread():
    while all_port:
        global procent
        global loading
        port = all_port.pop()
        procent += 1
        if procent % PROCENT_LOAD == 0:
            loading += "Ы"
            print('\rLoading: ' + loading, end="")
        if port_connect(adr, port):
            free_port.append(port)


adr = HOST
threads = [threading.Thread(target=port_thread) for i in range(HOWMUCH)]

[i.start() for i in threads]
[i.join() for i in threads]
print("\n")
print(len(loading))
print(sorted(free_port))
print(len(free_port))
