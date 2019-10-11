import socket
from collections import deque
from threading import Thread

THREADS_COUNT = 4
START_PORT = 5400
END_PORT = 5500


def check_port(port: int, host: str = 'localhost'):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if conn.connect_ex((host, port)):
        conn.close()
        return f'{host}:{port} is free'
    return f'{host}:{port} is not free'


def check_thread():
    while ports:
        print(check_port(ports.popleft()))


ports = deque(range(START_PORT, END_PORT))
threads = [Thread(target=check_thread) for _ in range(THREADS_COUNT)]
[i.start() for i in threads]
[i.join() for i in threads]
