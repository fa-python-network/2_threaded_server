import socket
import threading

m = 2 ** 16 - 1


def scan(arr):
    for port in arr:
        sock = socket.socket()
        try:
            sock.connect(('127.0.0.1', port))
            print("Порт", port, "открыт")
        except:
            continue
        finally:
            sock.close()
    return


for thread in range(66):
    arr = []
    for i in range(1000):
        arr.append(thread * 1000 + i)
        if arr[i] >= m:
            break
    thr = threading.Thread(target=scan, args=[arr])
    thr.start()
