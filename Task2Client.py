import socket


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



while True:#insert port
    print("Choose port")
    port=int(input())
    if 65535>=port>=1024:
        break
    print("Wrong port, try again!")
sock = socket.socket()
sock.connect((ip, port))
sock.send(ip.encode())
data = sock.recv(1024123)
print(data.decode())

msg = ''
while msg != "exit":
	msg = input()
	sock.send(msg.encode())
	data = sock.recv(1024123)
	print(data.decode())

sock.close()