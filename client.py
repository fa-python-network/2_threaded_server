import socket

sock = socket.socket()
host = input('Enter host name: ')

if host == 'localhost':

    pass

else:

    if any(c.isalpha() for c in host) == True:

        print('Incorrect host name entered. The local host is selected, by default')

        host = 'localhost'

    else:

        host_lst = host.split('.')           

        for i in host_lst:

            if 0 <= int(i) <= 255:

                pass

            else:
                host = 'localhost'
                print('Incorrect host name entered. The local host is selected, by default')

try:

    port = int(input('Enter port name: '))


    if 0 <= port <= 65535:
        pass

    else:

        print('Incorrect port name entered. Номер порта по умолчанию 9089')


        port = 9089

except ValueError:

    print("Incorrect port name entered. The default port number is 9089")


    port = 9089  

sock.connect((host, port))

print('Type exit to disconnect from the server')

msg = ''

while True:


    if msg != 'exit':

        print('Enter the message:')

        msg = input()

        sock.send(msg.encode())

        data = sock.recv(1024)
    else:

        break

sock.close()
print('Server operation completed.') 
