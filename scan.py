import socket
import threading

def scan(port, host, p_list):
    global bar
    sock = socket.socket()
    try:
        sock.connect((host, port))
        print('Обнаружен свободный порт')
        p_list.append(port)
    except:
        pass
    for i in range(10):
        if bar[i] == port:
            print(f"Progress: {(i+1)*10}|{'%'*(i+1)}")
            break
    sock.close()
p_list = []
host = input("Host: ")
if host == '':
    host = 'localhost'
bar = [int(65535*(i/10)) for i in range(1,11)]
thr = []
for port in range(65536):
    thr.append(threading.Thread(target = scan, args = [port, host, p_list]))
for i in thr:
    i.start()
for i in thr:
    i.join()
print("Free ports:")
p_list = sorted(p_list)
print(','.join(map(str, p_list)))
