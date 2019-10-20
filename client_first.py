import socket

sock = socket.socket()
port = input("Введите номер порта ")
try:
    port = int(port)
except:
    port = 4448
    print("Неправильный номер порта")

sock.connect(('localhost', port))
client_name = input("Введите своё имя")
if not client_name:
    client_name = "Client"
sock.send(client_name.encode())
while True:
    msg = input("Введите сообщение ")
    print("Sending data to server")
    sock.send(msg.encode())
    if msg == "exit":
        break


print("Получение информации с сервера")
data = sock.recv(1024)

print("Отключение")
sock.close()

print(data.decode())
