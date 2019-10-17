import threading
import socket

def scan_port(ip,port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(0.5)
  try:
     connect = sock.connect((ip,port))
     print('Порт с номером : ',port,' открыт')
     connect.close()
  except:
     pass

ip = '192.168.0.1'

for i in range(49000):
 potoc = threading.Thread(target=scan_port, args=(ip,i))
 potoc.start()