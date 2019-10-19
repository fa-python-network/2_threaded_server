import socket
import threading
import os
lock=threading.Lock()
lock2=threading.Lock()
lock3=threading.Lock()
class client(threading.Thread):
    def __init__(self,con,add):
        self.conn=con
        self.add=add
        print(3)
        self.name=self.log_in()
    def log_in(self):
        print(4)
        nameflag=0
        with lock:
            print(5)

            names = open('names.txt','r')
            print(6)
            for i in names:#check ip in names.txt
                print(i)
                print(self.add[0])
                if str(i.split(',')[0])[2:-1]==self.add[0]:#if ip is known
                    print(8)
                    nameflag=1#user is known
                    print(9)
                    name=i.split(',')[1][2:-1]
                    print(name)
                    message=str("Hello, {name}! Password please").encode()#send Hello, username!Password please
                    print(10)
                    self.conn.send(message)
                    print(11)
                    password_msg=(self.conn.recv(1024)).decode()
                    print(12)
                    password_txt+=password_msg
                    print(13)
                    
                    if i.split(',')[2][2:-3]==password_txt[:-1]:
                    #If password is right       
                            print("\nPassword is right")
                            check=True
                            break
                    if check==False:
                        print('\nPassword is wrong!')

            names.close()
        if nameflag==0:
            with lock3:
                self.conn.send(("Hello, stranger! What is your name?").encode())
                name=self.conn.recv(1024).decode()
                self.conn.send(("Nice to meet you, {name}! What is your password?").encode())
                password=(self.conn.recv(1024)).decode()
                names = open('names.txt','a')
                names.write(str([add,name,password])+"\n")
                users.append(name)
                names.close()
                
        return name
    def global_message(self,gl_msg):
        with lock2:#send to global chat file
            global_chat = open('global_chat.txt','w')
            global_chat.write(f"{self.name} global: {gl_msg}","\n")
            for userss in users:#send to all
                if userss!=self.name:
                    userss.conn.send((f"{self.name} global: {gl_msg}").encode)
    def message_to_user(self,target_user,us_msg):
        with lock2:#send to global chat file
            for userss in users:#send to all
                if userss==target_user:
                    userss.conn.send((f"{self.name} private: {gl_msg}").encode)
def menu():
    print(','.join(menu_list))
    while True:
        command = input('Enter the commands: ')
        if command == menu_list[0]:
            global_chat = open('global_chat.txt','r')
            for z in global_chat:
                print(z)
        #elif command == menu_list[1]:
         #   print("Enter username")
         #   username=input()
         #   print("Enter a message")
        #    msg_to_user=input()
        #    message_to_user(username,msg_to_user)
        #elif command == menu_list[2]:
         #   print("Enter a message")
        #    msg_glob=input()
         #   global_message(msg_glob)
        elif command == menu_list[3]:
            os.abort()

sock=socket.socket()
port=1024
while True:
    try:
        sock.bind(('', port))
    except: 
        port=port+1
    else:
        break 
print("Port is ",port)
users=[]
server_size=10
menu_list=["get_chat","message_to_user","global_message","exit"]
sock.listen(server_size)

thread = threading.Thread(target=menu)
thread.start()
while True:
    conn, addr = sock.accept()
    print(1)
    Client = client(conn, addr)
    print(2)
    Client.start()