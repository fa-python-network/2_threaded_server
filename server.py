import socket
from threading import Thread


class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] Добавлен новый клиент " + ip + ":" + str(port))

    def run(self):
        while True:
            data = conn.recv(2048)

            if data.lower() == 'exit' or data == '':
                print("[-] Клиент вышел " + self.ip + ":" + str(self.port))
                self.join()
                break
            conn.send(data.upper())  # echo



TCP_IP = '0.0.0.0'
TCP_PORT = 9092
BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(4)
    print("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip, port)) = tcpServer.accept()
    new_thread = ClientThread(ip, port)
    new_thread.start()
    threads.append(new_thread)

for t in threads:
    t.join()