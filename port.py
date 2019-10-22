# -*-coding: utf-8 -*-
import socket
import threading
import queue
import sys
from time import sleep

count = 0


def pb():
    global count
    while count < 65535:
        pr = int(count / 65535 * 100)
        sys.stdout.write('\r')
        sys.stdout.write(f'{"@"* pr:100}{pr}%')
        sys.stdout.flush()
        sleep(0.1)
    print('\nЗавершено')


def check(port, name_host, porti):
    global count
    sock = socket.socket()
    try:
        sock.connect((name_host, port))
        # print(f"Port is open {port}")
        porti.put(port)
    except:
        # print(f"Port is close {port}")
        pass
    finally:
        sock.close()
        count += 1



name_host = input('Введите host ')
spisok = []
porti = queue.Queue()
progress_bar = threading.Thread(target = pb)
progress_bar.daemon = True
progress_bar.start()
for port in range(65536):
    spisok.append(threading.Thread(target=check, args=[port, name_host, porti]))

for t in spisok:
    t.start()
for t in spisok:
    t.join()
# progress_bar.join()
s = []
while not porti.empty():
    s.append(porti.get())
print(s)
input()

