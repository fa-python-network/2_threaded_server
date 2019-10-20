import socket
import threading

CLIENT = 0  # количество всех клиентов, имеющих возможность одновременно подключаться
lock = threading.Lock()  # создает замок для всех потоков


def connect(conn: socket.socket, addr: tuple) -> None:
    """
    Функция подключения

    """

    print(addr[0])
    while True:
        data = conn.recv(1024)
        ans = data.decode()
        print(ans)
        if not data:
            break
        #"Я ловлю то, что ты присылаешь"
        conn.send(ans.upper().encode())
    conn.close()


sock = socket.socket()

try:
    num_port = int(input("Введите номер порта "))
    assert 1024 < num_port < 65535, "Ваше значение не удовлетворяет условию ввода. "

except (AssertionError, TypeError, ValueError) as e:
    num_port = 9091

print("Точка подключения: ", num_port)

sock.bind(("", num_port))
print('Успешно')

CLIENT = int(input("Введите количество прослушиваемых одновременно портов "))

sock.listen(CLIENT)


if __name__ == "__main__":

    while True:
     
        conn, addr = sock.accept()
        thread = threading.Thread(target=connect, args=[conn, addr])
        thread.start()
