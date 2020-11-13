import socket
import time

# Creaza un socket IPv4, TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectare la serverul care asculta pe portul 5000
s.connect(('127.0.0.1', 5001))

for i in range(3,10):
    # Trimite date
    s.sendall(bytes('Ana are ' + str(i) + ' mere', encoding="ascii"))
    # Asteapta date
    data = s.recv(1024)
    print('Am receptionat: ', data)
    # Asteapta o secunda
    time.sleep(1)
# Inchide conexiune
s.close()