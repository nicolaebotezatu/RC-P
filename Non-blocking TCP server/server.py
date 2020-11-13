import socket
import threading
import select
from pydispatch import dispatcher

def on_message_cb(message, signal):
    print('Am receptionat ', message, ' de la ', signal.getpeername())

def receive_fct():
    global running, client_list

    while running:
        if len(client_list) == 0:
            continue
        r, _, _ = select.select(client_list, [], [], 1)
        if r:
            for i in r:
                data = i.recv(1024)
                if not data:
                    print("Clientul a inchis conexiunea")
                    i.close()
                    client_list.remove(i)
                else:
                    dispatcher.send(message=data, signal=i)
                    #print("S-a receptionat ", str(data))
                    # Trimite inapoi datele receptionate
                    i.sendall(bytes('Clientul a trimis ' + str(data), encoding="ascii"))

# Creaza un socket IPv4, TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Asociere la adresa locala, portul 5000
s.bind(('127.0.0.1', 5001))
# Coada de asteptare pentru conexiuni de lungime 5
s.listen(5)

running = True
client_list =[]

try:
    receive_thread = threading.Thread(target=receive_fct)
    receive_thread.start()
except:
    print("Eroare la pornirea thread‐ului")

print('Asteapta conexiuni (oprire server cu Ctrl‐C)')
while 1:
    try:
        # Asteapta cereri de conectare, apel blocant
        # La conectarea unui client, functia returneaza un nou socket si o tupla ce contine adresa IP si portul clientului
        conn, addr = s.accept()
        client_list.append(conn)
        dispatcher.connect(on_message_cb, signal=conn)

    # La apasarea tastelor Ctrl‐C se iese din blucla while 1
    except KeyboardInterrupt:
        running = False
        receive_thread.join()
        print("Bye bye")
        break

    print('S‐a conectat clientul', addr)
    