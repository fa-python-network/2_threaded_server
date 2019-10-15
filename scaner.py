# -*-coding: cp1251-*-
import socket
import threading

count = 0


def scan(port, host):
    global count
    sock = socket.socket()
    try:
        sock.connect((host, port))
        print(f'Порт открыт {port}')
    except:
        # print(f'Порт закрыт {port}')
        pass
    finally:
        sock.close()
        count += 1
        x = int(count / 65535 * 100)
        print(")" * x)


host = input("vvedite host ")
lst = []
for port in range(65536):
    lst.append(threading.Thread(target=scan, args=[port, host]))
for t in lst:
    t.start()
for t in lst:
    t.join()
