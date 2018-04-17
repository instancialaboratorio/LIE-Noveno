"""
Se importan los módulo o librerías necesarias 
"""

import sys
import socket
from time import time
import time
import threading
from threading import Thread

# Hilo para enviar mensajes.

class HiloServidor(Thread):

    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket

   
    def run(self):
       
        while True:
            
            comando = input("Ingrese el comando: ")

            self.socket.send(bytes(comando, 'utf-8'))

            respuesta = str(self.socket.recv(2048), 'utf-8')
                
            print (respuesta)
            if respuesta == "desconectado":
                log = 1
                print("En 5 segundos se va cerrar la sesión: ...")
                time.sleep(5)
                self.socket.close()
                sys.exit()

            elif respuesta == "usuario ya existe":
                print ("usuario ya existe -.-")
                self.socket.close()
                sys.exit()

#Hilo para recibir mensajes

class HiloServidorLectura(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        socket2.connect((IP, PUERTO2))
        
        mensajeBienvenida = str(socket2.recv(2048), 'utf-8')
        
        chat = ""#Se declara la variable que va almacenar los mensajes que ingresan
        
        print (mensajeBienvenida)

        while True:
            if log == 0:
                
                chat= str(socket2.recv(2048), 'utf-8')
                print (chat)
                time.sleep(5)

            if log == 1:
                
                socket2.close()
                sys.exit()




"""
Inicio de programa principal
"""


IP = "127.0.0.1" #Dirección IP del servidor al que se debe conectar el cliente

PUERTO1 = int(5000) #Puerto de escucha del servidor de uno de los hilos

PUERTO2 = int(125) #Puerto de escucha del servidor de uno de los hilos


global log

hilos = []

log = 0


socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se crea el socket definido cmo "s"para establecer la comunicación con el servidor

socket1.connect((IP, PUERTO1)) #El socket "s" hace la solicitud de conexción con el servidor


"""
- estado 0 significa que el cliente no se ha identificado con su usuario y contraseña respectiva, entonces está desconectado del chat
- estado 1 el usuario está conectado al chat
- estado 2 el usuario está bloqueado


"""

estado = 0

while estado == 0:
    
    intentos = 0
    
    nombreUsuario = input("Ingrese el nombre de usuario: ")
    socket1.send(bytes(nombreUsuario, 'utf-8'))#Envía a través del socket el nombre de usuario digitado para que el servidor verifique si es válido
    
    verificacionNombreUsuario = str(socket1.recv(2048), 'utf-8')#Se recibe la verificación si el usuario es válido desde el servidor a través del socket

    if ( verificacionNombreUsuario == "Inicio de sesión inválido" ): #Si se recibe "Inicio de sesión inválido" significa que se digito un usuario no registrado
        
        print ("Nombre de usuario  inválido, ingrese los datos nuevamente")
        estado = 0
        
    else:
        if verificacionNombreUsuario == "mismo usuario": #Significa que ingresaron un usuario que ya está conectado
            
            estado = 1
            print ("El usario ya está conectado ¿Quién es usted?")
            print ("Por seguridad se va cerrar esta aplicación")
            time.sleep(5)
            sys.exit()
            
        else:
            while estado == 0:

                contrasena = input("Ingrese la contraseña: ")
                
                while len(contrasena) < 6:
                    print("La contraseña no cumple con los requisitos mínimos de longitud")
                    contrasena = input("Ingrese la contraseña: ")
                    
                socket1.send(bytes(contrasena, 'utf-8'))
                verificacionContrasena = str(socket1.recv(2048), 'utf-8')
                
                if ( verificacionContrasena == "entrada incorrecta" ):

                    estado = 0
                    intentos = intentos + 1
                    
                    if intentos == 3:
                        estado = 2
                        break
                    else:
                        print ("Contraseña inválida, ingresar nuevamente la contraseña")
                        
                else:
                    estado = 1


if intentos == 3: #and estado == 2: #Verifica si se ingresó de forma incorrecta la contraseña 3 veces

    print ("Realizó tres intentos fallidos de contraseña, será bloqueado por el sistema")
    time.sleep(5)
    sys.exit()

if ( estado == 1 ):
    print ("conectado")

    try:

        nuevoHilo1 = HiloServidor(socket1)
        nuevoHilo1.daemon = True
        
        nuevoHilo2 = HiloServidorLectura()
        nuevoHilo2.daemon = True
        
        nuevoHilo1.start()
        nuevoHilo2.start()

        hilos.append(nuevoHilo1)
        hilos.append(nuevoHilo2)

        
        while True:
            for t in hilos:
                t.join(600)
                if not t.isAlive():
                    break
            break
        

    except KeyboardInterrupt:
        comando = "desconectado"
        socket1.send(comando)
        sys.exit()
