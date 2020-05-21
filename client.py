import socket
import threading
import datetime

lock = threading.Lock()


def send_interface():
    global NICKNAME
    msg = ''
    print("===\n"
          "For closing the client type 'close'\n"
          "===")
    while True:
        time = datetime.datetime.now().time()
        msg = str(input("Message:\n"))
        if msg != 'close':
            output_data = str(time.strftime("%H:%M:%S ")) + NICKNAME + ": " + msg
            sock.send(output_data.encode())
        else:
            sock.close()
            print("You closed the chat")
            break


def receive_interface():
    while True:
        lock.acquire()
        data = sock.recv(1024)
        if data.decode() == 'bye':
            break
        print(data.decode())
        if not data:
            break
        lock.release()


NICKNAME = input("Enter your nickname:\n")
sock = socket.socket()
sock.setblocking(1)
sock.connect(('localhost', 9090))

threading.Thread(target=send_interface, daemon=False).start()
threading.Thread(target=receive_interface, daemon=False).start()
