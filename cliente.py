# Rojas Alvarez Robin Agustin
# Proyecto socket cliente

import socket
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(format='\tDEBUG : %(message)s', level=logging.DEBUG)
localhost = socket.gethostbyname(socket.gethostname())

# Clase cliente
class SocketClient:
    def __init__(self, puerto):
        self.puerto = puerto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (puerto, localhost)
        self.comunicacion = ThreadPoolExecutor(max_workers=10) #para ejecutar en paralelo
        self.mensaje = ""
        logging.debug("Cliente iniciado, escuchando en el puerto: {}".format(self.address))

    #conectar con el servidor
    def conectar(self):
        self.sock.connect(self.address)
        logging.debug("Conexion establecida")
    
    #enviar llave publica al servidor
    def enviar_llave(self, llave):
        self.sock.send(llave.encode())
        logging.debug("Llave publica enviada")

    #recibir llave publica del servidor
    def recibir_llave(self):
        llave = self.sock.recv(1024)
        logging.debug("Llave publica recibida: %s", llave)
        return llave

    #enviar mensaje al servidor a traves del socket
    def enviar_mensaje(self, msj):
        self.sock.send(msj.encode())
        logging.debug("Mensaje enviado: %s", msj)
        if msj != "salir":
            self.respuesta = ""

    #Analiza la información a enviar
    def escribir(self):
        while True:
            self.mensaje = input(">> ")
            if self.mensaje == "salir":
                break
            self.comunicacion.submit(self.enviar_mensaje, self.mensaje)
            self.comunicacion.submit(self.recibir_mensaje)

    #Recibe la respuesta del servidor
    def recibir_mensaje(self,):
        msj = ""
        while True:
            try:
                msj = self.sock.recv(1024).decode()
                logging.debug("Mensaje recibido: %s", msj)
                self.respuesta = msj
                if msj == "salir":
                    break
            except:
                print("Hubo un error de coneccion")
                break

    #cerrar conexion
    def cerrar_conexion(self):
        self.sock.close()
        logging.debug("Conexion cerrada")

    #ejecutar todo
    def ejecutar(self):
        self.conectar()
        self.escribir()
        self.cerrar_conexion()

    