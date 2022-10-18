import socket
import threading
import random
import time

# разворот сервера
print("Разворачиваемся...")
time.sleep(1)
random.seed()
sock = socket.socket()
port = 8001
try:
    sock.bind(('localhost', port))
except:
    port = random.randint(8002, 8600)
    sock.bind(('localhost', port))
print(f"Я на порту: {port}")
sock.listen(1)

# функция получения сообщения
def message_receiver(conn, addr, lst, user_num):
    while True:
        msg = conn.recv(1024).decode()
        print(f"User {user_num}: {msg}\n")
        if msg=='exit':
            lst.remove(conn)
            break
        else:
            alt_msg = f"User {user_num}: " + msg
            for i in lst:
                if i!=conn:
                    i.send(alt_msg.encode('utf-8'))
    print(f"User {user_num} отключился!\n")
    print("Количество клиентов")
    print(len(lst))
    print("Для отключения сервера нажмите Ctrl+C")
    conn.close()

# работа сервера: принятие соединения от клиентов
def server_work(lst):
    try:
        user_num=0
        print("Для отключения сервера нажмите Ctrl+C")
        while True:
            conn, addr = sock.accept()
            user_num+=1
            print(f"Подключился user {user_num}!")
            threading.Thread(target=message_receiver, args=(conn, addr, lst, user_num), daemon=True).start()
            lst.append(conn)
            print("Количество клиентов")
            print(len(lst))
    except KeyboardInterrupt:
        print("\nСворачиваемся\n")
        time.sleep(1)
        print("До свидания!")

lst=[]
server_work(lst)
