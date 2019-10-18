import socket, threading
import sys

def send(uname):
    while True:
        msg = input('\nI said: ')
        if msg == "exit":
            cli_sock.close()
            sys.exit()
            data = uname + ' has left'
        else:
            data = uname + ' said: ' + msg
            cli_sock.send(data.encode())

def receive():
    while True:
        data = cli_sock.recv(1024)
        print('\t'+ str(data.decode()))

if __name__ == "__main__":   

    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    HOST = 'localhost'
    PORT = 7777

    uname = input('Enter your name to enter the chat > ')

    cli_sock.connect((HOST, PORT))     
    print('Connected to remote host...')


    thread_send = threading.Thread(target = send,args=[uname])
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()
