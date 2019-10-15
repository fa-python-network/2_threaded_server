import socket
import time
from collections import deque
from threading import Thread

THREADS_COUNT = 4
START_PORT = 5400
END_PORT = 5440
HOST = 'localhost'


def check_port(port: int) -> dict:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if conn.connect_ex((HOST, port)):
        conn.close()
        return {port: True}
    return {port: False}


def check_thread():
    while ports:
        ports_result.update(check_port(ports.popleft()))


def progress_bar():
    count = len(ports)
    while ports:
        progress = int((1 - len(ports) / count) * 80)
        print('\rProgress ', '█' * progress + '░' * (80 - progress), end="")
        time.sleep(0.5)
    print('\rProgress ', '█' * 80, end="\n")


ports = deque(range(START_PORT, END_PORT))
ports_result = {}

threads = [Thread(target=check_thread) for _ in range(THREADS_COUNT)]
progress_bar_thread = Thread(target=progress_bar)
progress_bar_thread.start()
[i.start() for i in threads]
[i.join() for i in threads]
progress_bar_thread.join()
print([f'{HOST}:{k} is {"free" if v else "not free"}' for k, v in sorted(ports_result.items(), key=lambda x: x[0])])
