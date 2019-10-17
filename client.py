import socket

sock = socket.socket()
sock.setblocking(1)

host = input("Введите адрес хоста или lh: ")
if host == "lh":
	host = 'localhost'
else:
	host_ls = host.split(".", 4)
	for i in host_ls:
		if 0 <= int(i) <= 255:
			pass
		else:
			host = 'localhost'
port = int(input("Введите адрес порта: "))
if 1024 <= int(port) <= 65535:
	pass

sock.connect((host, port))
print('Введите Ваше сообщение или "exit" для выхода: ')
msg = ""
while True:
	cl_input = input()
	if cl_input == "exit".strip():
		a = 1
		print("Выходим из программы")
		break
	msg += cl_input + " "
sock.send(msg.encode())

print('Получаем ответ от сервера...')

if (a == 1) and (msg == ''):
	print('Disconnecting...')
	sock.close()
else:
	data = sock.recv(1024)
	print('Disconnecting...')
	sock.close()
	print("Вы ввели: ", data.decode())