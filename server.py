import threading
import socket


N = 2**16 - 1

def portscan(a):

    for n in range(a-1000, a):
        if n >=1:
            sock = socket.socket()
            sock.settimeout(1)
            try:
                sock.connect(('127.0.0.1', n))
                print("Порт :", n, "открыт")
            except:
                
                    sock.close()

                    pass


port_set = []
c = 0
b = 0

while True:
    if N >= b:
        b += 1000
        port_set.append(b)
        c += 1
    else:
        port_set[c-1] - 1000 + N % 1000
        break
                       
                              

print(port_set)
                      
thr = [threading.Thread(target=portscan, args=[a]) for a in port_set]
[t.start() for t in thr]
