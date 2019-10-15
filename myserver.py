import socket
class Myserver(socket.socket):
    def newmessage(self, lenght=None):
        length1 = int(self.recv(1).decode())
        length = self.recv(length1).decode()
        if lenght == '' or length == None:
            return ''
        length = int(length)
        message = self.recv(length).decode()
        return message

    def sendmessage(self, message):
        self.send(str(len(str(len(message)))).encode())
        self.send(str(len(message)).encode())
        self.send(message.encode())

    def newclient(self):
        fd, addr = self._accept()
        sock = Myserver(self.family, self.type, self.proto, fileno=fd)
        return sock, addr


