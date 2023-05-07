import socket
import pandas as pd
from io import StringIO
import random
import threading
import time


HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024
numConn = 4
listaConexiones = []
serveraddr = (HOST, int(PORT))
Gato = pd.DataFrame()
numrnd = 0
n = 0
nCeldas = 0
val = 2
mensaje = b" "
nivel = b" "
cont = 0
inicio = time.time()
fin = time.time()

def validar(m, car):
    if m == 3 and ((Gato.at[0, 'A'] == Gato.at[0, 'B'] == Gato.at[0, 'C'] == car) or \
                   (Gato.at[1, 'A'] == Gato.at[1, 'B'] == Gato.at[1, 'C'] == car) or \
                   (Gato.at[2, 'A'] == Gato.at[2, 'B'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'A'] == Gato.at[1, 'A'] == Gato.at[2, 'A'] == car) or \
                   (Gato.at[0, 'B'] == Gato.at[1, 'B'] == Gato.at[2, 'B'] == car) or \
                   (Gato.at[0, 'C'] == Gato.at[1, 'C'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'A'] == Gato.at[1, 'B'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'C'] == Gato.at[1, 'B'] == Gato.at[2, 'A'] == car)):
        if car == 'X':
            return 1
        if car == 'O':
            return 0
    elif m == 5 and (
            (Gato.at[0, 'A'] == Gato.at[0, 'B'] == Gato.at[0, 'C'] == Gato.at[0, 'D'] == Gato.at[0, 'E'] == car) or \
            (Gato.at[1, 'A'] == Gato.at[1, 'B'] == Gato.at[1, 'C'] == Gato.at[1, 'D'] == Gato.at[1, 'E'] == car) or \
            (Gato.at[2, 'A'] == Gato.at[2, 'B'] == Gato.at[2, 'C'] == Gato.at[2, 'D'] == Gato.at[2, 'E'] == car) or \
            (Gato.at[3, 'A'] == Gato.at[3, 'B'] == Gato.at[3, 'C'] == Gato.at[3, 'D'] == Gato.at[3, 'E'] == car) or \
            (Gato.at[4, 'A'] == Gato.at[4, 'B'] == Gato.at[4, 'C'] == Gato.at[4, 'D'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[0, 'A'] == Gato.at[1, 'A'] == Gato.at[2, 'A'] == Gato.at[3, 'A'] == Gato.at[4, 'A'] == car) or \
            (Gato.at[0, 'B'] == Gato.at[1, 'B'] == Gato.at[2, 'B'] == Gato.at[3, 'B'] == Gato.at[4, 'B'] == car) or \
            (Gato.at[0, 'C'] == Gato.at[1, 'C'] == Gato.at[2, 'C'] == Gato.at[3, 'C'] == Gato.at[4, 'C'] == car) or \
            (Gato.at[0, 'D'] == Gato.at[1, 'D'] == Gato.at[2, 'D'] == Gato.at[3, 'D'] == Gato.at[4, 'D'] == car) or \
            (Gato.at[0, 'E'] == Gato.at[1, 'E'] == Gato.at[2, 'E'] == Gato.at[3, 'E'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[0, 'A'] == Gato.at[1, 'B'] == Gato.at[2, 'C'] == Gato.at[3, 'D'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[4, 'A'] == Gato.at[3, 'B'] == Gato.at[2, 'C'] == Gato.at[1, 'D'] == Gato.at[0, 'E'] == car)):
        if car == 'X':
            return 1
        if car == 'O':
            return 0
    else:
        return 2

def Ini_Juego(Client_conn):
    global numrnd
    global n
    global nCeldas
    global Gato
    global nivel
    global inicio

    while True:
        nivel = Client_conn.recv(buffer_size)
        if nivel == b"principiante":
            n = 3
            strGto = """A;B;C\n ; ; \n ; ; \n ; ; """
            Client_conn.sendall(str.encode(strGto))
            numrnd = [0, 1, 1, 2]
            break
        elif nivel == b"avanzado":
            n = 5
            strGto = """A;B;C;D;E\n ; ; ; ; \n ; ; ; ; \n ; ; ; ; \n ; ; ; ; \n ; ; ; ; """
            Client_conn.sendall(str.encode(strGto))
            numrnd = [0, 0, 1, 1, 2, 2, 2, 3, 4, 4]
            break
        Client_conn.sendall(b"Ingrese una cadena valida")
    nCeldas = n * n
    Gato = pd.read_csv(StringIO(strGto), sep=";")
    inicio = time.time()

def Juego(Client_conn):
    global val
    global mensaje
    global cont

    while True:
        celda = Client_conn.recv(buffer_size)
        columna = chr(celda[0])
        fila = chr(celda[1])
        if ((n == 3) and ((columna == 'A' or columna == 'B' or columna == 'C') and (
                fila == '0' or fila == '1' or fila == '2'))) or ((n == 5) and (
                (columna == 'A' or columna == 'B' or columna == 'C' or columna == 'D' or columna == 'E') and (
                fila == '0' or fila == '1' or fila == '2' or fila == '3' or fila == '4'))):
            if Gato.at[int(fila), columna] == ' ':
                coor = columna + fila
                print("Se recibio la coordenada:", coor)
                Gato.at[int(fila), columna] = 'X'
                cont = cont + 1
                val = validar(n, 'X')
                if (cont < nCeldas) and val == 2:
                    cont = cont + 1
                    while True:
                        filcol = random.sample(numrnd, 2)
                        if (filcol[0] == 0):
                            columna = 'A'
                        elif (filcol[0] == 1):
                            columna = 'B'
                        elif (filcol[0] == 2):
                            columna = 'C'
                        elif (filcol[0] == 3):
                            columna = 'D'
                        elif (filcol[0] == 4):
                            columna = 'E'
                        if Gato.at[filcol[1], columna] == ' ':
                            break
                    mensaje = (columna + str(filcol[1]))
                    Gato.at[filcol[1], columna] = 'O'
                    val = validar(n, 'O')
                    if val == 2:
                        envio = (Gato.to_csv(index=False))
                        envio = envio.replace(',',';').encode()
                        Client_conn.sendall(envio)
                        print("Se envio la coordenada:", mensaje)
                    else:
                        break
                else:
                    break
            else:
                Client_conn.sendall(b"La coordenada esta ocupada:")
        else:
            Client_conn.sendall(b"Ingrese una coordenada valida:")

"""Acepta conexiones entrantes de clientes y crea un nuevo hilo para cada conexión.
   Además, gestiona la lista de conexiones activas utilizando la función gestion_conexiones."""
def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            #Se agrega el objeto de conexión a la lista de conexiones listaconexiones.
            listaconexiones.append(client_conn)
            #Se crea un nuevo hilo para cada conexión aceptada, que llamará a la función recibir_datos
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            #El hilo se inicia con el método start().
            thread_read.start()
            #Se llama a la función gestion_conexiones para gestionar las conexiones activas.
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

"""Se encarga de eliminar las conexiones que ya no están activas y de imprimir información sobre
   el estado del servidor, como el número de hilos activos y la lista de conexiones activas."""
def gestion_conexiones(listaconexiones):
    """Se itera sobre cada conexión de la lista de conexiones listaconexiones si el método fileno()
       del objeto de conexión devuelve -1, se elimina la conexión de la lista utilizando remove()"""
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    #threading.active_count() devuelve el número de hilos activos en el servidor.
    print("hilos activos:", threading.active_count())
    #threading.enumerate() devuelve una lista de todos los hilos en ejecución.
    print("enum", threading.enumerate())
    #len(listaconexiones) devuelve la cantidad de conexiones activas en la lista.
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)

def recibir_datos(conn, addr):
    global fin
    try:
        print("Recibiendo datos del cliente:",addr)
        if nivel == b" ":
            print("Esperando eleccion de nivel... ")
            Ini_Juego(conn)
        Juego(conn)
        print("Salimos de la funcion juego")
        if val == 1:
            conn.sendall(b"Ganaste")
        elif val == 0:
            print("Se envio la coordenada:", mensaje)
            conn.sendall(b"Perdiste")
        elif val == 2:
            conn.sendall(b"Empataste")
        envio = (Gato.to_csv(index=False))
        envio = envio.replace(',', ';').encode()
        time.sleep(1)
        conn.sendall(envio)
        fin = time.time()
        seg = int(fin) - int(inicio)
        min = int(seg / 60)
        segf = seg - (min * 60)
        time.sleep(1)
        conn.sendall(str(min).encode())
        time.sleep(1)
        conn.sendall(str(segf).encode())
    except Exception as e:
        print(e)
    finally:
        for conn in listaConexiones:
            conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)
