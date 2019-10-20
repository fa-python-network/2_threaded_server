import socket
import threading

def check(host, port):
    global sc_ports
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc_ports += 1
    try:
        sock.connect((host, port))
        return port
    except:
        return False

def progress_bar():
    while ports:
        global percent
        global progress_line
        port = ports.pop()
        percent += 1
        if percent % round(65535/100) == 0:
            progress_line += "#"
            print('\rПрогресс',len(progress_line),'% : ' + progress_line, end="")
            if  len(progress_line) == 100:
                print ('|')
        if check(host, port):
           opened_ports.append(port)


host = input('Введите имя хоста для сканирования портов: ')
if host == '':
    host = 'localhost'
print('Start...')
    
opened_ports = []
ports = []
sc_ports = 0
amount = 3000
percent = 0
progress_line = ""



for i in range(65535):
    ports.append(i)
  

for i in range(amount):
    thr = threading.Thread(target = progress_bar)
    thr.start()
    thr.join()
    

print("\n\n------ Результаты:")
print('Просканированно портов: ', sc_ports)
print('Открытых портов: ', len(opened_ports))
print(sorted(opened_ports))

