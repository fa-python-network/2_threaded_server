# -*- coding: utf-8 -*-
import socket, csv
from threading import Thread
    
    
def numport():
    '''Функция выбора порта.'''
    while True:
        try:
            portnum = int(input("Write port number\n"))
            if 1024 <= portnum <= 65535:
                break 
            else: 
                print("Wrong format of port number")
     
        except:
            print("Wrong format of port number, default set")
            portnum = 9090
            break
        
    return portnum


def ask_send(conn, ask):
    '''Функция отправления сообщения.
    
    Принимает conn и само сообщение.
    
    '''
    conn.send(ask.encode())
    
    
def msg_recv(conn, pr = 0, name = 'Client'):
    '''Функция принятия сообщения.
    
    Принимает conn, а также необязательные параметры:
    pr -- нужно ли выводить сообщение на экран (default 0)
    name -- имя клиетна (default "Client")
    
    '''
    data = conn.recv(1024).decode()
    if pr:
        print(f"{name}: {data}")
        
    return data


def binding(sock, portnum):
    '''Функция бинда.
    
    Принимает сокет и номер порта.
    
    '''
    while True:
        try:
            sock.bind(('', portnum))
            print("Using port:", portnum)
            break
            
        except:
            portnum += 1
            print ("Using port:", portnum)
            
            
def client(conn, addr):
    '''Функция основной работы с клиентом.
    
    Принимает conn и адрес клиента.
    
    '''
    print(addr,"connected")
    try:
        name = ident(conn, addr)
        while True:
            try:
                data = msg_recv(conn,1,name)
                if not data:
                    print("No message recieved")
                    conn.close()
                    break
                
                if data == "exit":
                    print(f"{name} exits")
                    conn.close()
                    break
            
            except:
                conn.close()
                break
                
            ask = input("Server: ")
            ask_send(conn, ask)
            
    except:
        print("Possibly was checked, disconnect")
        conn.close()
    
    
def recogn(line, conn):
    '''Функция узнавания при авторизации.
    
    Принимает строчку (список) из файла клиентов и conn.
    
    '''
    ask_send(conn, "I know you. Enter password:")
    
    while True:
        pswd = msg_recv(conn)
        if line[2] == pswd:
            ask_send(conn, "Welcome, " + line[1])
            break
        else:
            ask_send(conn, "Wrong password, try again:")
            
            
def not_recogn(conn, addr):
    '''Функция НЕузнавания при авторизации.
    
    Принимает conn и адрес клиента.
    
    '''
    ask_send(conn, "Who are you?")
    
    try:
        name = msg_recv(conn, 1)
        ask_send(conn, "Choose password")
        pswd = msg_recv(conn, 1)
        
    except:
        name = "Guest"
        ask_send(conn, "Wrong format of name. I would call you a guest.")
        ask_send(conn, "Choose Password")
        pswd = msg_recv(conn)
        
    with open ("list.csv", "a") as inls:
        csv.writer(inls).writerow([addr[0], name, pswd])
        inls.close()
    
    ask_send(conn, "Welcome, " + name)
    
    return name
    
    
def ident(conn, addr):
    '''Функция идентификации.
    
    Принимает conn и адрес клиента.
    
    '''
    known = False
    with open("list.csv", "r") as ls:
        for line in csv.reader(ls):
            # Если сервер узнал клиента:
            if line[0] == addr[0]: 
                recogn(line, conn)
                known = True
                name = line[1]
                break
        ls.close()
    # Если сервер не узнал клиента:    
    if not known:                  
        name = not_recogn(conn, addr)
        
    return name
                
                
    
            
def main():
    '''Основная функция.'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    binding(sock, numport())
    sock.listen(2)
    try:
        while True:
            conn, addr = sock.accept()
            Thread(target = client, args = (conn, addr)).start()
            
    finally:
        sock.close()


#===========================================
        
main()
