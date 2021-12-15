# Rojas Alvarez Robin Agustin
# proyecto, parte 1

from concurrent.futures.thread import ThreadPoolExecutor
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import binascii
import base64
from pathlib import Path
import logging
from datetime import datetime
import json
from server import SocketServer
from cliente import SocketClient


class ObjetoSeguro: #clase principal para crear objetos seguros
    def __init__(self, nombre: str, puerto:int):
        self.nombre = nombre
        logging.debug("Objeto : %s", self.nombre) # registra objeto
        self.__privkey = ""
        self.__pubKeyHex = 00
        self.__privkeyHex = ""
        self.code = 0
        self.code_msj = 0
        self.base64_msj = 0
        self.__registro = {}
        self.socket_server = SocketServer(puerto)
        self.socket_client = SocketClient(puerto)
        self.comunicacion = ThreadPoolExecutor(max_workers=10)
        self.escribir = ""
        self.recibir_mensaje = ""
        self.llave_publicaserver = ""
        self.llave_publicacliente = ""



    def gen_llaves(self): # genera llaves
       self.__privKey = generate_eth_key()
       self.__privKeyHex = self.__privKey.to_hex()
       self.__pubKeyHex = self.__privKey.public_key.to_hex()
       print("Llave publica de cifrado: ", self.__pubKeyHex)
       print("Llave privada de cifrado: ", self.__privKeyHex)


    def llave_publica(self)->str:
       return self.__pubKeyHex

    # codifica mensaje en base64
    def codificar64(self,msj:str)->bytes:
        self.base64_msj = base64.b64encode(msj.encode())
        print("Mensaje codificado: ", self.base64_msj)
        return self.base64_msj

    # decodifica mensaje en base64
    def decodificador64(self, msj):
        self.base64_msj = base64.b64decode(msj)
        print("Mensaje decodificado: ", self.base64_msj)
        return self.base64_msj
        
    # cifra mensaje con la llave publica
    def cifrar_msj(self, pub_key, msj):
        msj_cifrado = encrypt(self.__pubKeyHex, msj)
        print("Mensaje cifrado: ", msj_cifrado)
        return msj_cifrado
       
    # descifra mensaje con la llave privada
    def decifrar_msj(self, msj):
        msj_decifrado = decrypt(self.__privKeyHex, msj)
        print("Mensaje decifrado: ", msj_decifrado)
        return msj_decifrado       

    #inicio de comunicación 
    def saludar(self, name: str, msj: str):
        print(f"Hola, soy {name} y quiero decir {msj}")
        return f"Hola, soy {name} y quiero decir {msj}" 

    # Responde mensaje
    def responder(self, msj):
        print(f"Hola, recibi el mensaje {msj}")
        

    # guarda mensaje en archivo
    def almacenar_msj(self, msj):
        self.__id= 0
        self.__id += 1
        d = datetime.now().strftime("%A, %d %B, %y %H:%M%S ")
        archivo = "RegistoMsj_<" + self.nombre + ">.json"
        idstr = str(self.__id)
        self.__registro["{ID:<"+idstr +" }"] = {
            "ID":self.__id,
            "Usuario": self.nombre,
            "Mensaje": msj,
            "fecha": d}
        with open(archivo, 'w') as f:
            json.dump(self.__registro, f, indent=5)
        print("{ID:<"+ idstr + ">}")
        return "{ID:<"+ idstr + ">}"

    
    # consulta mensaje en archivo
    def consultar_msj(self, id):
        archivo = "RegistoMsj_<" + self.nombre + ">.json"
        with open(archivo, 'r') as f:
            self.__registro = json.load(f)
        print(self.__registro)
        return self.__registro

    # espera respuesta, recibe el mensaje cifrado, decifra y almacena en archivo
    def esperar_respuesta(self, msj): 
       print ("Esperando respuesta...")
       mensaje = self.decifrar_msj(msj)
       mensaje = self.decodificador64(mensaje)
       self.almacenar_msj(mensaje)
       print("Mensaje recibido: ", mensaje)

    def comunicacion(self): 
        self.socket_server.incia_servidor()
        self.socket_client.conectar
        self.recibir_mensaje = self.socket_client.enviar
        self.intercambio_seguro()
        logging.debug("Objeto : %s", self.nombre) # registra objeto
        self.socket_client.escribir
        self.socket_server.recibir

    def servicio_server(self):
        self.gen_llaves()
        self.socket_server.inicia_servidor()
        self.socket_server.enviar_mensaje(self.llave_publica())
        self.socket_server.recibir(self.decodificar64())

    def servicio_cliente(self):
        self.socket_client.conectar()
        self.socket_client.enviar(self.llave_publica())
        self.socket_client.recibir_llave()
        self.socket_client.enviar(self.codificar64(self.saludar(self.nombre, "Hola")))
        self.socket_client.escribir(self.codificar64())


    def intercambio_seguro(self): # intercambio de llaves
        self.socket_client.enviar(self.llave_publica())
        self.llave_publicacliente = self.socket_server.recibir_llave()
        self.socket_server.enviar(self.llave_publica())
        self.llave_publicaserver = self.socket_client.recibir_llave()
        print("Llave publica del servidor: ", self.llave_publicaserver)
        print("Llave publica del cliente: ", self.llave_publicacliente)

    def shutdown(self):
        if not self.escribir.done() and self.recibir_mensaje.done():
            self.escribir.cancel()
            self.recibir_mensaje.cancel()
            self.socket_server.shutdown()
            self.socket_client.shutdown()
            print("Se ha desconectado el servidor")
            print("Se ha desconectado el cliente")






#Objeto1 = ObjetoSeguro("Objeto1")
#Objeto1.gen_llaves()
#mensaje = "Hola Mundo"
#Objeto1.codificar64(mensaje)
#Objeto1.decodificador64(Objeto1.codificar64(mensaje))
#Objeto1.cifrar_msj(Objeto1.llave_publica(), Objeto1.base64_msj)
#Objeto1.decifrar_msj(Objeto1.cifrar_msj(Objeto1.llave_publica(), Objeto1.base64_msj))
#Objeto1.almacenar_msj(Objeto1.base64_msj)
#Objeto1.consultar_msj(Objeto1.almacenar_msj(Objeto1.base64_msj))
