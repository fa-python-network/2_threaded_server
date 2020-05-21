import socket
import threading

N = 2**16 - 1


def scanning(n):
    print("Начат поток", n)
    for port in range(n-1000, n):
        if port >= 1:
            sock = socket.socket()
            try:
                print("Проверка порта ", port)
                sock.connect(('127.0.0.1', port))
                print("Порт", port, "открыт")
            except:
                continue
            finally:
                sock.close()
    print("Закрыт поток ", n)


port_list = []
i = 0
m = 0
while True:
    if m <= N:
        m += 1000
        port_list.append(m)
        i += 1
    else:
        port_list[i-1] = port_list[i-1] - 1000 + N % 1000
        break

print(port_list)
threads = [threading.Thread(target=scanning, args=[n]) for n in port_list]
[t.start() for t in threads]

