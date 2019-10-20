import socket
import threading
import progressbar

def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = f'Порт {port_number} открыт'
    except:
        output[port_number] = ''


def scan_ports(host_ip, delay):
    global bar
    progress = 0
    threads = []        # Потоки
    output = {}         # Результаты

    # Создание потоков для сканирования
    for i in range(65535):
        t = threading.Thread(target=TCP_connect, args=(host_ip, i, delay, output))
        threads.append(t)
        progress += 1
        bar.update(progress)

    # Запеуск потоков
    threads_counter = 0
    while threads_counter < 65535:
        for i in range(0 + threads_counter, 10000 + threads_counter):
            try:
                threads[i].start()
            except IndexError:
                break
            progress += 1
            bar.update(progress)
        # Блокировка основного потока до завершения всех потоков
        for i in range(0 + threads_counter, 10000 + threads_counter):
            try:
                threads[i].join()
            except IndexError:
                break
            progress += 1
            bar.update(progress)

        threads_counter += 10000
    bar.finish()
    # Вывод на печать
    for i in range(65535):
        if output[i]:
            print(output[i])


def main():
    host_ip = input("Enter host IP: ")
    delay = 1
    scan_ports(host_ip, delay)


if __name__ == "__main__":
    bar = progressbar.ProgressBar(maxval=196605).start()
    main()