import socket
import pandas as pd
from io import StringIO

HOST = "127.0.0.1"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024
Gato = pd.DataFrame()
data = b" "
min = ' '
seg = ' '

def Ini_Juego(TCPClientSocket):
    global data
    while True:
        nivel = input("Ingresa el nivel: ")
        TCPClientSocket.sendall(str.encode(nivel))
        data = TCPClientSocket.recv(buffer_size)
        if data == b"Ingrese una cadena valida":
            print(data.decode())
        elif data == b"Ingrese una coordenada valida:":
            break
        else:
            Gato = pd.read_csv(StringIO(data.decode()), sep=";")
            print(Gato)
            break

def Juego(TCPClientSocket):
    global Gato
    global data
    global min
    global seg

    while True:
        coordenada = input("Ingresa tu coordenada a tirar (ejemplo A1): ")
        TCPClientSocket.sendall(str.encode(coordenada))
        data = TCPClientSocket.recv(buffer_size)
        if ((data != b"Ingrese una coordenada valida:") and (data != b"La coordenada esta ocupada:")):
            if (data != b"Perdiste" and data != b"Ganaste" and data != b"Empataste"):
                Gato = pd.read_csv(StringIO(data.decode()), sep=";")
                print(Gato)
            else:
                dato = TCPClientSocket.recv(buffer_size)
                Gato = pd.read_csv(StringIO(dato.decode()), sep=";")
                print(Gato)
                print(data.decode())
                min = TCPClientSocket.recv(buffer_size).decode()
                seg = TCPClientSocket.recv(buffer_size).decode()
                break
        else:
            print(data.decode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    Ini_Juego(TCPClientSocket)
    Juego(TCPClientSocket)
    print("El juego duró:",min,"min",seg,"seg")
    TCPClientSocket.close()
