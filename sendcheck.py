from time import sleep

# Общие функции отправки и принятия сообщения.

def sendmsg(who, msg):
    sleep(0.1)
    msg_len = str(len(msg))
    while len(msg_len) < 5:
        msg_len = msg_len + "+"
    who.send((msg_len + msg).encode())


def checkmsg(who):
    msg_len = who.recv(5).decode()
    if msg_len == "":
        return ""
    msg_len = int(msg_len.replace('+', ''))
    msg = who.recv(msg_len*2).decode()
    return msg
