import socket
from datetime import datetime
from contextlib import closing
import os
import hashlib
import json
import pickle
from threading import Thread
import sys
from time import sleep


class Server():

   def __init__(self,log = "file.log", users = "users.json", clients = [], status = None):
       self.__log = log
       self.__users = users
       self.clients = clients
       self.port =  int(input("Порт:"))
       self.sock = None
       self.status = status
       self.startServer()

   def startServer(self):
       self.sock = socket.socket()
       while True:
           try:
               self.sock.bind(('',self.port))
               break
           except:
               self.port+=1
       print(f'Занял порт {self.port}')
       self.sock.listen(5)
       while True:
           conn, addr = self.sock.accept()
           self.serverStarted(addr)
           Thread(target = self.listenToClient,args = (conn,addr)).start()
           self.clients.append(conn)

   def broadcast(self,msg, conn):
       try:
           open('messages.txt').close()
       except FileNotFoundError:
           open('messages.txt', 'w').close()
       with open('messages.txt', "a") as f:
           f.write(msg)
           f.write('\n')
       for sock in self.clients:
           if sock != conn:
               data = pickle.dumps(["message",msg])
               sock.send(data)

   def checkPasswrd(self, passwd, userkey) -> bool:
       key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
       return key == userkey

   def generateHash(self, passwd) -> bytes:
       key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
       return key

   def listenToClient(self, conn, address):
       conn.send(pickle.dumps(["nameRequest",""]))
       client = pickle.loads(conn.recv(1024))[1]
       self.checkUser(address,conn, client)
       self.loadAllmessages(conn)
       while True:
               data = conn.recv(1024)
               if data:
                   status , data = pickle.loads(data)
                   if status == "message":
                       self.broadcast(data, conn)
               else:
                   conn.close()
                   msg=f"{client} has left at {datetime.now().time()}"
                   self.broadcast(msg,conn)
                   self.clients.remove(conn)
                   self.serverStopped(address)
                   break
   def loadAllmessages(self,conn):
       with open("messages.txt", "r") as f:
           for line in f:
               sleep(0.3)
               conn.send(pickle.dumps(["message",line]))


   def serverStarted(self,ip):
       with open(self.__log, "a", encoding="utf-8") as f:
           print(f"{datetime.now().time()} Server Launched {ip}", file=f)
           
           
   def serverStopped(self,ip):
       with open(self.__log, "a", encoding="utf-8") as f:
           print(f"{datetime.now().time()} Server Stopped {ip}", file = f)


   def newUser(self,conn, users,client):
       conn.send(pickle.dumps(["nameRequest",""]))
       client = pickle.loads(conn.recv(1024))[1]
       conn.send(pickle.dumps(["passwd","Я вас еще не знаю, поэтому придумайте себе пароль : "]))
       passwd = self.generateHash(pickle.loads(conn.recv(1024))[1])
       conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"]))
       users[client] = {'password': passwd}
       print(users)
       msg=f"{client} has connected at {datetime.now().time()}"
       print(msg)
       self.broadcast(msg,conn)
       with open(self.__users, "w", encoding="utf-8") as f:
           json.dump(users,f)


   def checkUser(self, addr, conn,client):
       try:
           open(self.__users).close()
       except FileNotFoundError:
           open(self.__users, 'a').close()
       with open(self.__users, "r") as f:
           try:
               conn.send(pickle.dumps(["nameRequest",""]))
               client = pickle.loads(conn.recv(1024))[1]
               users = json.load(f)
               try:
                   name = users[client]
                   conn.send(pickle.dumps(["passwd","Введите свой пароль: "]))
                   passwd = pickle.loads(conn.recv(1024))[1]
                   conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"])) if self.checkPasswrd(passwd,name['password']) else self.checkUser(addr,conn)
                   msg=f"{client} has connected at {datetime.now().time()}"
                   self.broadcast(msg,conn)
               except: self.newUser(conn,users)
           except:
               conn.send(pickle.dumps(["nameRequest",""]))
               client = pickle.loads(conn.recv(1024))[1]
               conn.send(pickle.dumps(["passwd","Я вас еще не знаю, поэтому придумайте себе пароль :  "]))
               passwd = self.generateHash(pickle.loads(conn.recv(1024))[1])
               conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"]))
               msg=f"{client} has connected at {datetime.now().time()}"
               self.broadcast(msg,conn)
               with open(self.__users, "w", encoding="utf-8") as f:
                   json.dump({client : {'password': passwd} },f)




server = Server()

