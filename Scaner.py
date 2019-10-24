import socket
from contextlib import closing
import threading


def chek_ports(a=0, b=65535):
    for i in range(a, b + 1):
        chek_port(i)


def chek_port(port, host='localhost'):
    global s
    global count
    global free_ports
    with threading.Lock():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex((host, port)) == 0:
                free_ports.append(str(port))
        count += 1
        if count % 512 == 0:
            print(chr(9632), end='')


if __name__ == '__main__':
    free_ports = []
    count = 0
    threads = []
    # Методом научного тыка самый оптимальный вариант - 8
    shag = 8
    print("Сканирую свободные порты:")
    print('0%' + ' '*137 + '100%')
    for i in range(0, 65536-shag, shag):
        t = threading.Thread(target=chek_ports, args=[i, i + shag])
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print()
    print("Сканирование завершено\nСвободные порты:")
    print(', '.join(sorted(free_ports, key=int)))