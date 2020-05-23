import socket
import logging
import threading

logging.basicConfig(
    filename='server.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.DEBUG
)

logging.debug('\n')
logging.debug('Запуск сервера')

sock = socket.socket()  # инициализация сокета
sock.settimeout(60)

# Задаётся базовый порт
port = int(input("Введите порт: "))

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
    
    
while True:
    try:
        sock.bind(('', port))
    except socket.error:
        logging.warning('Порт %s занят, поиск другого', port)
        port += 1
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
            sock.shutdown(socket.SHUT_RDWR)
        except (socket.error, OSError, ValueError):
            pass
        break


sock.close()
logging.debug('Сервер остановлен')
