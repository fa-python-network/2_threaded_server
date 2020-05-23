import socket
import logging

# Установлен конфиг для логирования
import threading

logging.basicConfig(
    filename='server.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.DEBUG
)

logging.debug('-----------------------------------')
logging.debug('Сервер запущен')

sock = socket.socket()  # Инициализация сокета
sock.settimeout(60)  # Установлен интервал бездействия


def connect(conn, addr):
    logging.debug('Клиент подключен, информация о нём: %s', addr)

    logging.debug('Обмен сообщениями с клиентом')
    while True:
        data = conn.recv(1024)
        if not data or data.decode() == "exit":
            logging.debug('Клиент завершил обмен')
            break
        logging.debug('Сообщение от %s: %s', addr, data.decode())
        conn.send(data)
    conn.close()
    logging.debug('Клиент отключен')
    return


# Задаётся базовый порт
while True:
    try:
        while True:
            port = int(input("Введите порт (диапозон 1024-65535): "))
            if 1024 <= port <= 65535:
                break
    except ValueError:
        print("Повторите ввод!")
    else:
        break

# Проверка доступности порта. Перебор, в случае неудачи
while True:
    try:
        sock.bind(('', port))  # Занимаем порт
    except socket.error:
        logging.warning('Порт %s занят, поиск другого', port)
        port += 1
        if port > 65536:
            logging.warning('достигнут предел диапозона портов')
            port = 1024
    else:
        logging.debug('Назначен порт %s', port)
        break

logging.debug('Прослушивание порта')
sock.listen(1)

while True:
    logging.debug('Ожидание подключения клиента')
    try:
        conn, addr = sock.accept()  # Установка соединени с клиентом
        thr = threading.Thread(target=connect, args=[conn, addr])
        thr.start()
    except socket.timeout:
        try:
            logging.warning('Сервер бездействует, остановка ..')
            sock.shutdown(socket.SHUT_RDWR)  # Завершение работы сокета, в случае бездействия
        except (socket.error, OSError, ValueError):
            pass
        break

sock.close()
logging.debug('Сервер остановлен')
