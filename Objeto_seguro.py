# Rojas Alvarez Robin Agustin
# proyecto, parte 1

from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import binascii
import base64
from pathlib import Path
import logging
from datetime import datetime

class ObjetoSeguro:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.__privkey = ""
        self.__publicKeyHex = 00
        self.__privkeyHex = ""
        self.code = 0
        self.code_msj=0
        self.base64_msj = 0


    def gen_llaves(self):
       self.__privKey = generate_eth_key()
       self.__privKeyHex = self.__privKey.to_hex()
       self.__pubKeyHex = self.__privKey.public_key.to_hex()
       print("Llave publica de cifrado: ", self.__pubKeyHex)
       print("Llave privada de cifrado: ", self.__privKeyHex)

    def saludar(self, name:str, msj:str):
        self.code_msj = self.codificar64(msj)
        print(f"Hola, soy {name} y esta es mi llave publica {self.__pubKeyHex}")
        return f"Hola, soy {name} y esta es mi llave publica {self.__pubKeyHex}", self.code_msj

    def responder(self, msj:str):
        pass

    def llave_publica(self)->str:
        return self.__pubKeyHex

    def cifrar_msj(self, pub_key, msj):
        msj = msj.encode()
        self.code = encrypt(self.__pubKeyHex, msj)
        self.code = binascii.hexlify(self.code)
        print("Mensaje cifrado", self.code)
        return self.code

    def decifrar_msj(self, msj):
        decode_msj = binascii.a2b_hex(self.code)
        decode_msj = decrypt(self.__privKeyHex, decode_msj)
        print("Mensaje decifrado", decode_msj)
        return decode_msj


    def codificar64(self,msj:str)->bytes:
        msj_cod = msj.encode('ascii')
        base64_bytes = base64.b64encode(msj_cod)
        self.base64_msj = base64_bytes.decode("ascii")
        print ("Mensaje codificado base64", self.base64_msj)
        return self.base64_msj

    def decodificador64(self, msj):
        base64_bytes = self.base64_msj.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        messaje = message_bytes.decode('ascii')
        print("mensaje decodificado", messaje)
        return messaje

    #def almacenar_msj(self, msj):
        #id= 0
        #dicc = {}
        #if Path ("./mensajes.txt").stat().st_size =! 0:
            #with open ("./mensajes.txt", "w"):
                #dicc[f'{id}']={
             #      "ID: ": id,
              #     "Mensaje: ": msj,
               #    "De: ": self.nombre,
                #   "fecha :": str(datetime.now().strftime("%A, %d of %B %Y at %I:%M %p"))
            #}
            #return dicc

    #def consultar_msj(self, id:int):
        #logging.debug(f'que # de mensaje quieres consultar?{id}')
        #if Path ('./mensajes.txt').stat().st_size !=0:
            #with open("./mensajes.txt", "r"):
              #  num_mensaje = dicc[f'{id}']
#                return num_mensaje

    def esperar_respuesta(self, msj):
        descifrar = self.decifrar_msj(msj)
        decodificar = self.decodificador64(descifrar)
        print("Recibi: ", decodificar, "de: ", self.nombre)
        #self.almacenar





Objeto1 = ObjetoSeguro("Juan")

Objeto1.gen_llaves()
nombre = input("escriba su nombre, por favor")
mensaje = input("Escriba el mensaje que desea enviar")
Objeto1.saludar(nombre, mensaje)
Objeto1.cifrar_msj("pub_key", mensaje)
Objeto1.decifrar_msj(mensaje)
Objeto1.codificar64(mensaje)
Objeto1.decodificador64(mensaje)
Objeto1.almacenar_msj(mensaje)
