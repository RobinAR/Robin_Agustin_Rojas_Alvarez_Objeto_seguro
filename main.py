# Rojas Alvarez Robin Agustin
# Proyecto, main.py -> instanciación

from Objeto_seguro import ObjetoSeguro

if __name__ == "__main__":
    #Comienza la instaciación del objeto1
    nombre = input("Ingrese el nombre del objeto: ")
    puerto = int(input("Ingrese el puerto del objeto: "))
    rol = input("Ingrese el rol del objeto C=cliente/S=servidor: ")
    if rol =="C":
        objeto=ObjetoSeguro(nombre,puerto)
        objeto.servicio_cliente()
    elif rol=="S":
        objeto=ObjetoSeguro(nombre,puerto)
        objeto.servicio_server()


    print("Ingrese un rol valido")
    


