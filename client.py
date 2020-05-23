# coding=utf-8
import socket

ip = "127.0.0.1"
port = 8080
sock = socket.socket()
sock.connect((ip, port))
sock.sendall(bytes("Я новый клиент", 'UTF-8'))

while True:
    data = sock.recv(1024)
    print("От сервера :", data.decode())
    out_data = input()
    sock.sendall(bytes(out_data, 'UTF-8'))
    if out_data == 'bye' or out_data=='':
        print ('Всего хорошего')
        break
sock.close()