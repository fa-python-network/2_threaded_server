import socket
import threading
import Taskclient1
def get_message():
    print('xxx')
    while True:
        print(b)
        msg=sock.recv(1024).decode()
        print(msg)
while True:#insert ip
    print("Choose ip")
    ip=input()
    ip1=ip.split(".")
    if ip=="":
        ip="localhost"
        break
    if ip =="localhost":

        break
    c=0
    
    for i in ip1:
        if 255>=int(i)>=0:
            c=c+1
    if c==4:
        break   
    print("Mistakes were made....")

sock = socket.socket()
sock.setblocking(0)
print("Do you want me to show you all ports? Yes/No")
question=input()
if question!="No":
    Taskclient1.check_all_ports(ip)

while True:
    print("Choose port")
    port=int(input())
    if 65535>=port>=1024:
        break
    print("Wrong port, try again!")
sock.connect((ip,port))
rec=threading.Thread(target=get_message)
rec.start()
msg=''
while msg!='exit':
    msg=input()
    if msg=='exit':
        break
    sock.send(msg.encode())
sock.close()