import socket
import threading

# get local IP
# IP = socket.gethostbyname(socket.gethostname())
IP = '0.0.0.0'
PORT = 7345
STRING_ID = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((IP, PORT))

s.send(bytearray('INIT_CONN', 'UTF-8'))

payload = bytearray('msg', 'UTF-8')

for i in range(5):
    s.send(payload)
# data = s.recv(1024)
s.send(bytearray('CLOSE_CONN', 'UTF-8'))

s.close()

# print("receive data:", data)