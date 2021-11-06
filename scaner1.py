import threading
from datetime import datetime

import socket

start = datetime.now()

def scanning(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        connect = sock.connect((ip, port))

        print('Порт ', port, 'открыт')
        sock.close()
    except:
        pass



for i in range(1000):
    potoc = threading.Thread(target=scanning, args=("mail.ru", i))
    potoc.start()

end = datetime.now()
print(f"Time: {end-start}")
