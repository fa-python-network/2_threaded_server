import socket
import threading
import os

def check_port(ip,i):
    try:
        sock = socket.socket()
        sock.settimeout(0.00001)
        sock.connect((ip,i))
    except:
        pass          
    else:
        free_ports.append(i)
    sock.close()
        
free_ports=[]
threads=[]
percent=[65536//10*i for i in range(1,11)]

while True:#Inporting and checking ip
    print("Choose ip")
    ip=input()
    ip1=ip.split(".")
    if ip =="localhost":

        break
    if ip=="":
        ip="localhost"
        break
    c=0
    
    for i in ip1:
        if 255>=int(i)>=0:
            c=c+1
    if c==4:
        break   
    print("Mistakes were made....")

j=0
for i in range(65537):
    new_thread=threading.Thread(target=check_port,args=[ip,i])
    threads.append(new_thread)
    new_thread.start()
    #Printing process bar
    if j!=10 and i==percent[j]:
        print(f"{(j+1)*10}%:{(j+1)*10*'#'}", end='')
        print('\r', end='')
        j+=1

     
for new_thread in threads:
    new_thread.join()
print("\n",free_ports)

