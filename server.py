import socket
import re
import time
import json
import threading

lgf = open("logfile.txt", "a+")
users_current = dict()

def udata_mgmt():
    try:
        users_source = open("users_list.json", "r")
        usrs = users_source.read()
        users_current = json.loads(usrs)
        users_source.close()
        print("READING USERS LIST\n\n")
    except:
        print("CREATED USERS LIST\n\n")

def user_management(new_host):
    
    if new_host in list(users_current.keys()):
        conn.send(("\n_____________HELLO_____________, "+users_current[new_host]+"\n").encode())
    else:
        conn.send(("WELCOME TO THE SYSTEM, REGISTERING "+new_host+"\n"+
            "Vvedite imya, pod kotorym vas zapomnit sistema:\n").encode())

        name = conn.recv(1024).decode()
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa", name)
        conn.send(("REGISTERED USER" + ' "' + name + '" ' + "SUCCESSFULLY\n").encode())
        users_current.update({new_host: name})

#     users_out = open("users_list.json", "w+")
#     json.dump(users_current, users_out)
#     users_out.close()

def checker():
    port = "4000"
    host = "localhost"
    print("default host is 127.0.0.1(localhost)\n"
          "default port is 4000"
          )
    while True:
        uhost = input("vvedite host:\n")
        if uhost == "default" or uhost == "localhost" or uhost == "lh":
            break
        elif re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', uhost) == None:
            print("try again")
        else:
            host = uhost
            break
    while True:
        uport = input("vvedite port:\n")
        if uport == "default" or uport == "4000":
            break
        elif not uport.isnumeric() == True or int(uport)<1024 or int(uport) > 65535:
            print("try again")
        else:
            port = uport
            break
    resu = [host, int(port)]
    return resu

def process(conn, addr):
    msg = ""
    # lgf.write(time.ctime() + f"\nCONNECTION FROM IP = {addr[0]} PORT = {addr[1]}\nMESSAGES:\n\n")
    print(time.ctime() + f"\nCONNECTION FROM IP = {addr[0]} PORT = {addr[1]}\nMESSAGES:\n\n")
    thr = threading.Thread(target=user_management, args=(addr[0], ))
    thr.start()
    thr.join()
    while True:
        try:
            data = conn.recv(1024)
        except:
            print(time.ctime() + "\nCLIENT DISCONNECTED\n\n")
            # lgf.write(time.ctime() + "\nCLIENT DISCONNECTED\n\n")
            break
        if not data:
            print(time.ctime() + "\nCLIENT DISCONNECTED\n\n")
            # lgf.write(time.ctime() + "\nCLIENT DISCONNECTED\n\n")
            break
        msg += data.decode()
        # conn.send(data)
        # lgf.write(data.decode()+"\n\n")
        print(data.decode()+"\n\n")


udata_mgmt()

res = checker()
sock = socket.socket()
while True:
    try:
        print("\nTRYING PORT =", res[1], "\n")
        sock.bind((res[0], res[1]))
        break
    except:
        print("PORT ALREADY IN USE, TRYING THE NEXT ONE\n")
        res[1] += 1

sock.listen(2)
print("SERVER IS ON PORT", res[1])
# lgf.write(time.ctime()+"\nSERVER UP AND RUNNING\nLIST OF CONNECTIONS:\n\n")
print(time.ctime()+"\nSERVER UP AND RUNNING\nLIST OF CONNECTIONS:\n\n")

while True:
    try:
        conn, addr = sock.accept()
        t = threading.Thread(target=process, args=(conn, addr) )
        t.start()
    except:
        print("fuck off")
        break

conn.close()
lgf.close()
