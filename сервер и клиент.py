# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 08:58:00 2019

@author: 184150
"""
### Server
import socket
import threading
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

while True:
     data = conn.recv(1024)
     if not data:
         break
     conn.send(data.upper())

conn.close()

### Client


sock = socket.socket()
sock.connect(('localhost', 9090))
sock.send('hello, world!')

data = sock.recv(1024)
sock.close()

print (data)
 

def proc(n):
   print ("Процесс", n)
 
p1 = threading.Thread(target=proc, name="t1", args=["1"])
p2 = threading.Thread(target=proc, name="t2", args=["2"])
p1.start()
p2.start()

