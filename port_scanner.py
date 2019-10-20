import socket
import threading
import time

threads = []

def port(ip, port):
    sock = socket.socket()
    try:
        sock.connect((ip, port))
        print(f"Порт {port} открыт")
    except (ConnectionError, OSError):
        pass
    sock.close()


ip_ = input("Выберите ip: ")
time_start = time.time()
port_n = 0 # Текущий порт
while port_n < 65536:
    if threading.active_count() < 440: # Потому что у меня на ноуте ограничение по кол-ву потоков
        t = threading.Thread(target=port, args=(ip_, port_n))
        t.start()
        threads.append(t)
        port_n+=1


threads[-1].join()

time_res = time.time() - time_start
print(time_res)

