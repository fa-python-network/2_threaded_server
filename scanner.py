import threading, socket, time, math

ip = input('Введите ip адрес сканируемого существа: ')
num = 1285
floaters = []
ports = []
opens = []


def scaner(rng):
    """
    Принимает список номеров портов в int
    """
    global ports
    global opens
    for i in rng:
        sock = socket.socket()
        sock.settimeout(0.1)
        # sock.setblocking(1)
        try:
            sock.connect((ip, i))
            ports.append(i)
            opens.append(i)
        except:
            ports.append(1)
            continue

# range(65535)[1:15]

def create_potok(num):  # всего потоков 4369
    global floaters
    shag = int(65535 / num)

    for i in range(num):
        floaters.append(threading.Thread(target=scaner, args=(range(shag * i + shag)[shag * i:],)))
        floaters[-1].start()

def processing():  # Заполнение шкалы прогресса
    counted = 0
    while True:
        time.sleep(1)
        if math.floor((len(ports) / 65535) * 100) > counted:
            counted = math.floor((len(ports) / 65535) * 100)
            print("|", end="")
        if counted >= 100:
            print('//')
            break

def work():
    create_potok(num)
    print('loading \\\\', end='')
    processing()
    print(opens)

work()
print('thx for using me')
