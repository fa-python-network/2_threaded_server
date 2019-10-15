# -*-coding: utf-8 -*-
import socket
import threading

count = 0


def check(port, name_host, porti):
    global count
    sock = socket.socket()
    try:
        sock.connect((name_host, port))
        # print(f"Port is open {port}")
        porti.append(port)
    except:
        # print(f"Port is close {port}")
        pass
    finally:
        sock.close()
        count += 1
        proverka = int(count / 65535 * 80)
        print("@" * proverka)


name_host = input('Введите host ')
spisok = []
porti = []
for port in range(65536):
    spisok.append(threading.Thread(target=check, args=[port, name_host, porti]))

for t in spisok:
    t.start()
for t in spisok:
    t.join()
print(porti)
input()
