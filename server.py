# Rojas Alvarez Robin Agustin
# Proyecto socket server

import socket
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(format='\tDEBUG : %(message)s', level=logging.DEBUG)
localhost = socket.gethostbyname(socket.gethostname())

#Clase servidor
class SocketServer:
    def __init__(self, puerto:int):
        self.puerto = puerto
        self.address= (puerto, localhost)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        self. sesiones = []
        self.comunicacion = ThreadPoolExecutor(max_workers=10) #para ejecutar en paralelo
        self.mensaje = ""
        logging.debug("Servidor iniciado, escuchando en el puerto: {}".format(self.address))

    def bind(self): #para escuchar
        self.sock.bind(self.address)

    #abrir canal para escuchar
    def escuchar(self):
        self.sock.listen(10)
        logging.debug("Escuchando...")
    
    #aceptar conexiones
    def aceptar_comunicacion(self):
        while True:
            cliente, address = self.sock.accept() 
            logging.debug("Cliente conectado: %s", address) 
            self.sesiones.append(cliente) #agregar cliente a la lista de sesiones
            self.comunicacion.submit(self.recibir, cliente) 

    #recibir llaver publica del cliente
    def recibir_llave(self, cliente):
        llave_cliente = cliente.recv(1024)
        logging.debug("Llave recibida: %s", llave_cliente)
        return llave_cliente

    #recibir mensaje del cliente
    def recibir(self, msj):
        while True:
            try:
                msj = self.sock.recv(1024).decode()
                logging.debug("Mensaje recibido: %s", msj)
            except:
                print("Hubo un error de coneccion")
                break
    
    #enviar mensaje al cliente
    def enviar_mensaje(self, msj):
        self.sock.send(msj.encode())
        logging.debug("Mensaje enviado: %s", msj)

    #cerrar conexion
    def cerrar_conexion(self):
        self.sock.close()
        logging.debug("Conexion cerrada")

    #metodo para iniciar el servidor y la comunicacion
    def inicia_servidor(self):
        self.bind()
        self.escuchar()
        self.aceptar_comunicacion()
        self.recibir_llave()
        
    