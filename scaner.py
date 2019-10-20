import socket
import threading
import queue


def scanner(host: str, num: int, que: queue.Queue) -> None:
    g = num
    while (num != g + 546) and num < 65535:
        try:

            scan = socket.socket()
            scan.connect((host, num))
            que.put(num)

        except OSError:
            pass
            
        finally:
            num += 1
            scan.close()

if __name__ == "__main__":
        
    scan = socket.socket()
    num_port = 1
    host_name = input("Любезнейший, прошу вас, введите имя хоста ")
    NUM = 120
    threads = []

    que = queue.Queue()  # открытые порты

    port = 547  # количество обрабатываемых каждым потоком портов

    for i in range(NUM):
        new_thread = threading.Thread(target=scanner, args=[host_name,port, que])
        new_thread.start()
        port += 546  # каждый следующий поток рассматривает на 546 больше

    for thread in threads:
        thread.join()

    ports = []
    while not que.empty():
        ports.append(que.get())
    
    print(*sorted(ports),sep = '; ')

