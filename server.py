import json
import threading
from myserver import Myserver
sock = Myserver()
freeHost = 1025
while True:
    try:
        if freeHost == 65536:
            print('All ports busy')
            break
        sock.bind(('', freeHost))
        break
    except:
        freeHost += 1
print(freeHost)
print("Server starts")
sock.listen(0)

def newclient (conn, addr):
    while True:
        print(f"{addr[0]}")
        with open("dataClients.json", "r+") as d:    #проверка пользователя с помощью файла
            data = json.loads(d.read())
            for i in data['clients']: #цикл на проверку пользователя
                if i['ip'] == addr[0]:
                    conn.sendmessage(f'Hello, {i["name"]} , enter the password:')
                    while True:
                        passw = conn.newmessage()
                        if passw == i['password']:
                            conn.sendmessage('Password is Correct')
                            break
                        conn.sendmessage('It\'s Not Correct, try again')
                    break
            else: #добавление нового
                conn.sendmessage('Hello, You\'re new, please enter you name ')
                name = conn.newmessage()
                conn.sendmessage('And you\'re secret password ')
                password= conn.newmessage()
                newclient = {"ip": addr[0], "name": name, "password": password}
                data['clients'].append(newclient)
                d.seek(0)
                d.write(json.dumps(data))
                conn.sendmessage('congratulation')

        data = ''
        while True:
            data = conn.newmessage()
            if data == "exit":
                break
            print(data)
        conn.close()
        break
        return

while True:
    conn, addr  = sock.newclient()
    t1 = threading.Thread(target=newclient, args=[conn, addr])
    t1.start()





