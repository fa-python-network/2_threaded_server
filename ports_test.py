import socket
import time
from threading import Thread

THREADS_COUNT = 1000
START_PORT = 0
END_PORT = 65300
HOST = 'localhost'


class PortsHolder:
    active = True

    def __init__(self, start: int, end: int):
        self._port = start
        self.start = start
        self.end = end
        self.get_port = self._get_port()

    def _get_port(self) -> iter:
        while self.active:
            port = self._port
            self._port += 1
            if self._port == self.end:
                self.active = False
            yield port

    def __len__(self):
        return self.end - self._port


def check_port(port: int) -> dict:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if conn.connect_ex((HOST, port)):
        conn.close()
        return {port: True}
    return {port: False}


def check_thread():
    while ports.active:
        ports_result.update(check_port(next(ports.get_port)))


def progress_bar():
    count = len(ports)
    while ports.active:
        progress = int((1 - len(ports) / count) * 80)
        print('\rProgress ', '█' * progress + '░' * (80 - progress), end="")
        time.sleep(0.5)
    print('\rProgress ', '█' * 80, end="\n")


ports = PortsHolder(START_PORT, END_PORT)
ports_result = {}

threads = [Thread(target=check_thread) for _ in range(THREADS_COUNT)]
progress_bar_thread = Thread(target=progress_bar)
progress_bar_thread.start()
[i.start() for i in threads]
[i.join() for i in threads]
progress_bar_thread.join()
print([f'{HOST}:{k} is not free' for k, v in sorted(ports_result.items(), key=lambda x: x[0]) if not v])
