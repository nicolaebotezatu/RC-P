import socket
import threading

def comm_thread(conn, addr):
    while 1:
        # Asteapta date, buffer de 1024 octeti (apel blocant)
        data = conn.recv(1024)
        # Daca functia recv returneaza None, clientul a inchis conexiunea
        if not data:
            break
        print(addr, ' a trimis: ', data)
        # Trimite inapoi datele receptionate
        conn.sendall(bytes(str(addr) + ' a trimis ' + str(data), encoding="ascii"))
    print("Clientul ", addr, " a inchis conexiunea")
    conn.close()

# Creaza un socket IPv4, TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Asociere la adresa locala, portul 5000
s.bind(('127.0.0.1', 5000))
# Coada de asteptare pentru conexiuni de lungime 5
s.listen(5)

print('Asteapta conexiuni (oprire server cu Ctrl‐C)')
while 1:
    try:
        # Asteapta cereri de conectare, apel blocant
        # La conectarea unui client, functia returneaza un nou socket si o tupla ce contine adresa IP si portul clientului
        conn, addr = s.accept()

    # La apasarea tastelor Ctrl‐C se iese din blucla while 1
    except KeyboardInterrupt:
        print("Bye bye")
        break

    print('S‐a conectat clientul', addr)
    try:
        threading.Thread(target=comm_thread, args=(conn, addr)).start()
    except:
        print("Eroare la pornirea thread‐ului")