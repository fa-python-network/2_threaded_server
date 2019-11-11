import socket

sock = socket.socket()

host = input('Write host name: ')
if host == 'localhost':
    pass
else:
    if any(c.isalpha() for c in host) == True:
        print('Host name is incorrect. Local host selected by default')
        host = 'localhost'
    else:
        host_lst = host.split('.')           
        for i in host_lst:
            if 0 <= int(i) <= 255:
                pass
            else:
                host = 'localhost'
                print('Host name is incorrect. Local host selected by default')

try:
    port = int(input('Write port number: '))
    if 0 <= port <= 65535:
        pass
    else:
        print('Port number is incorrect. Port number is 9090 by default')
        port = 9090
        
except ValueError:
    print("Port number is incorrect. Port number is 9090 by default")
    port = 9090  

sock.connect((host, port))

print('Write exit to stop working with server')
msg = ''

while True:
    if msg != 'exit':
        print('Write message:')
        msg = input()
        sock.send(msg.encode())
        data = sock.recv(1024)
    else:
        break
    
sock.close()
print('Work with server is over.') 