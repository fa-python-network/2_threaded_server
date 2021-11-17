

import threading
from datetime import datetime
import time
from progress.bar import IncrementalBar

k = 1000

bar = IncrementalBar('Progress', max=k)

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


for i in range(k):
    potoc = threading.Thread(target=scanning, args=("mail.ru", i))
    potoc.start()
    bar.next()



end = datetime.now()
bar.finish()

print(f"Time: {end - start}")


