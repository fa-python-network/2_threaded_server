import socket
from tqdm import tqdm
import time
import threading

def ask_send(sock, ask):
    '''Функция отправки сообщения. 
    
    Принимает сокет и само сообщение.
    
    '''
    sock.send(ask.encode())


def msg_recv(sock):
    '''Функция принятия сообщения. 
    
    Принимает сокет.
    
    '''
    try:
        data = "Server: " + sock.recv(1024).decode()
        print(data)
        return data
    
    except:
        print("disconnect")


def scanner(host):
    '''Функция реализации сканера. 
    
    Принимает имя хоста.
    
    '''
    opened = []
    for i in tqdm(range(20000)):
        ...
        threading.Thread(target=ch_port, args=(host, i, opened)).start()
        
    opened.sort()
    return opened   # Возвращаем список открытых портов


def ch_port(host, i, opened):
    '''Функция подключения-отключения сокета к портам. 
    
    Принимает имя хоста, номер порта и список открытых портов.
    
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('localhost', i))
        opened.append(i)
        
    except(ConnectionError, OSError):
        pass
    sock.close()
        
    
def numport(ports):
    '''Функция выбора порта. 
    
    Принимает список возможных портов.
    
    '''
    while True:
        try:
            portnum = int(input(f"Write port number from {ports}\n"))
            if 1024 <= portnum <= 65535:
                break
            else:
                print("Wrong format of port number")

        except:
            print("Wrong format of port number")
            
    return portnum
        

def hostname():
    '''Функция выбора хоста.'''
    while True:
        try:
            host = input("Write host address\n")
            for i in host.split("."):
                if 255 < int(i) or int(i) < 0:
                    print("Wrong format of hostname")
                    break
            break

        except:
            print("Wrong format of hostname, set default")
            host = "localhost"
            break
            
    return host


def auth(sock):
    '''Функция авторизации. 
    
    Принимает сокет.
    
    '''
    while True:
        data = msg_recv(sock)
        
        # Если серверу не знаком наш адрес:
        if "Who are you?" in data:  
            name = input()
            ask_send(sock, name)
            
        # Когда сервер просит придумать пароль или ввести его:    
        if "password" in data:  
            pswd = input()
            if pswd != "":
                ask_send(sock, pswd)
            else:
                print("Password set as 'pswd'")
                pswd = "pswd"
                ask_send(sock, pswd)
                
        # Когда мы успешно авторизировались:        
        if "Welcome" in data:   
            name = data.split()[1]
            break
        
    return name
    

def talking(sock, name):
    '''Функция общения. 
    
    Принимает сокет и имя клиента.
    
    '''
    threading.Thread(target=msg_recv, args=(sock,)).start()
    msg = ''
    while msg != 'exit':
        msg = input(f'{name}: ')
        ask_send(sock, msg)


def main():
    '''Основная функция.'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = hostname()
    ports = scanner(host)   # Запускаем сканер для нахождения открытых портов
    port = numport(ports)
    
    try:
        sock.connect((host, port))
        name = auth(sock)
        talking(sock, name)
        
    finally:
        sock.close()

#=============================================
        
main()
