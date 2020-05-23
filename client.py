import socket
from time import sleep

sock = socket.socket()

host = input('������� ��� �����:')
if host == 'localhost':
    pass
else:
    if any(c.isalpha() for c in host) == True:
        print('������������ ��� �����.�� ��������� ��������� ����')
        host = 'localhost'
    else:
        host_lst = host.split('.')
        for i in host_lst:
            if 0 <= int(i) <= 255:
                pass
            else:
                host = 'localhost'
                print('������������ ��� �����.�� ��������� ��������� ����')

try:
    port = int(input('����� �����:'))
    if 0 <= port <= 65535:
        pass
    else:
        print('������������ ����� �����. ���� �� ��������� 9090')
        port = 9090

except ValueError:
    print("������������ ����� �����. �� ��������� 9090")
    port = 9090

sock.connect((host, port))

print('exit ��� ���������� ������ � ��������')
msg = ''