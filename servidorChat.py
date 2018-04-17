"""
Importación de los módulos necesarios predetermindados de Python que son necesarios para utilizar en el programa.

"""
import socket
import sys
import collections
import time
import queue
import threading
from threading import Thread
from socketserver import ThreadingMixIn


"""
Clase construida, denominada HiloCliente. Esta clase lo que hace es manejar un hilo exclusivo en el programa servidor para manejar la conexión
y comunicación de cada cliente en específico.

Como es una clase construida que va manejar hilos, entonces hereda de la clase Threand de Python.

Al momento de crear un ejemplar de esta clase en el programa, la clase recibe como parametro un objeto socket, la ip y puerto del cliente.

"""
 
class HiloCliente(Thread):
    #A continuación el método cosntructor de la clase
    def __init__(self,socket,ip,puerto):
        Thread.__init__(self)
        self.socket = socket
        self.ip = ip
        self.port = puerto
        print ("Un nuevo hilo inició para manejar la conexión de un cliente del chat")
    #A continuación el método run de la clase
    def run(self):
        estado = 0  # Variable que define el estado del cliente, 0 si está desconectado, 1 si está conectado, 2 si está bloqueado
        """
        Variable que representa el estado de un usuario cuando está presente en el archivo de usuarios y contraseñas
        0 cuando no está presente
        1 cuando está presente

        """
        usuarioPresente = 0 # Variable que define si un usario es parte de la lista de usuarios que existen en el archivo de usuarios. 0 no está presente y 1 está presente

        while True: #Ciclo infinito del hilo hasta que sea interrumpido
                                 
            datoClaveParaEnviar = "exitoso"#Se inicializa la variable con la palabra exitoso
            
            while usuarioPresente == 0: #Ciclo que se repite mientras el valor de la variable usuarioPresente se igual a 0
                
                intentos = 0 #Variable que controla los intetos de ingreso de contraseña
                
                nombreUsuario = str(self.socket.recv(1024), 'utf-8')# Se recibe a través del socket el usuario que se está  iniciando sesión en el cliente y se guarda en la variable
     
                listaUsuariosContrasenas = open('usuariosContrasenas.txt').readlines() #Instrucción que abre el archivo y devuelve una lista con los datos que tiene el archivo

                """
                Por ejemplo:
                
                ['allan 123456\n', 'sebas 123456\n', 'stefano 123456\n', 'morera 123456\n', 'gabriela 123456\n', 'pedro 123456\n', 'carlos 123456\n', 'andres 123456\n', 'karla 123456\n']
                
                """

                
                for registroUsuario in listaUsuariosContrasenas: # Ciclo for que analiza cada uno de los registros de la lista denominda listaUsuariosContrasenas
                    
                    # Instrucción que divide cada uno de los registros de la lista listaUsuariosContrasenas y lo alamcena temporalmente en otra lista denominda datosUsuarios
                    #Por ejemplo ['sebas', '123456\n']
                    
                    datosUsuarios = registroUsuario.split(" ")
                
                    #Condicional que compara el nombre de usuario recibido del cliente contra el primer elemento de la lista datosUsuarios
                    #para verificar si es un usuario registrado
                    if nombreUsuario == datosUsuarios[0]:
                        usuarioPresente = 1 #Se le asigna el valor 1 a la variable usuarioPresente
                        datoClaveParaEnviar = "exitoso"
                        
                if usuarioPresente == 0: #Condicional que verifica si el usuario no estaba presente       
                        
                    datoClaveParaEnviar = "Inicio de sesión inválido" # Se le asigna el mensaje "Inicio de sesión inválido" a la variable datoClaveParaEnviar
                    estado = 0 #Se le asigna a la variable estado 0 dado que no era un usuario válido
                    print (datoClaveParaEnviar) #El servidor reporta por pantalla el Inicio de sesión inválido
                    
                    self.socket.send(bytes(datoClaveParaEnviar, 'utf-8')) #Se envía al cliente a través del socket que es un Inicio de sesión inválido
                
                else: # En caso de que si sea un usuario válido
               
                    for usuario in usuariosActuales: #Ciclo que recorre la lista de usuarios actuales conectados
                        print ("Usuario ",usuario," está actualmente conectado") #El servidor reporta por pantalla los usuarios actuales conectados
                        
                        if nombreUsuario == usuario: #Condicional que verifica si el usuario que está intentado conectarse, ya es uno de los usuarios conectados
                            datoClaveParaEnviar = "mismo usuario" #Almacena en la variable datoClaveParaEnviar la cadena "mismo usuario" para enviar al cliente, para indicarle que ya está conectado
                            estado = 1 # Se asigna 1 a estado porque ya está conectado
                            
                    if datoClaveParaEnviar == "mismo usuario": #Verifica que la variable trae el dato "mismo usuario" para enviar eso al cliente a través del socket
                        self.socket.send(bytes(datoClaveParaEnviar, 'utf-8')) # Envía al cliente el dato respectivo a través del socket
                        estado = 1 # Se asigna 1 a estado porque ya está conectado
                        
                    
            """
            Condicional que verifica si la variable trae el valor "exitoso" que significa que el usuario del cliente que se está conectando es válido
            
            """
            if datoClaveParaEnviar == "exitoso": 
                
                self.socket.send(bytes(datoClaveParaEnviar, 'utf-8')) #Se envía el dato al cliente a través del socket para que haga el ingreso de contraseña
       
                contrasenaPresente = 0 #Variable que va definir si la contraseña que envíe el cliente es válida
                
                while estado == 0: # Ciclo que se ejecuta mientras la variable estado sea igual a 0
                    
                    contrasenaUsuario = str(self.socket.recv(1024),'utf-8')# Se recibe del cliente la contraseña con la que se desea autenticar
                    
                    """
                    Une el nombre de usuario más constraseña en una variable denomida "validacion"
                    para verificar si es un usuario correcto en el archivo de usuarios y contraseñas

                    ejemplo: "allan 123456"
                    """
                    validacion = nombreUsuario + " " + contrasenaUsuario
                   
                    if (validacion not in open('usuariosContrasenas.txt').read()): # Verifica que el usuario y contraseña está en el archivo de usuarios y contraseñas
                        
                        datoClaveParaEnviar = "entrada incorrecta" # Si el usuario no está asigna el valor "entrada incorrecta" a la variable datoClaveParaEnviar
                        print (datoClaveParaEnviar) # Reporta por pantalla en el servidor el valor de la variable datoClaveParaEnviar
                        
                        intentos = intentos + 1 # Le suma 1 a la variable intentos, va controlando cuántas veces intenta ingresar la contraseña 
                        
                        if intentos == 3: # Si la variable intentos es igual a 3 significa que se ingresó la contraseña incorrecta tres veces
                            self.socket.send(bytes(datoClaveParaEnviar, 'utf-8')) # Se enviá al cliente el dato "entrada incorrecta"
                            print ("Se va interrumpir el hilo de conexión con el cliente, porque tiene 3 intentos fallidos de contraseña")#Reporte por pantalla en el servidor
                            break       
                        else: 
                            estado = 0 
                        
                            self.socket.send(bytes(datoClaveParaEnviar, 'utf-8')) # Se enviá al cliente el dato "entrada incorrecta"
                            
                    else: # Se ingresa aquí si el usuario y contraseña ingresados es de un usuario válido
                        
                        datoClaveParaEnviar = "exitoso"
                        
                        self.socket.send(bytes(datoClaveParaEnviar, 'utf-8')) # Se envía al cliente que el ingreso fue exitoso
                        

                        """
                        Ciclo for que revisa en la lista de usuarios deconectados si el usuario estaba desconectado para eliminarlo de esa lista
                        """                       
                        bloqueo.acquire() #Bloquea el hilo       
                        usuariosActuales.append(nombreUsuario) # Agrega el usuario a la lista de usuarios conectados
                        bloqueo.release() #Libera el hilo
                        
                        print (nombreUsuario + " conectado...") # Reporta por panatalla que el usuario está conectado
                        
                        estado = 1 # Se asigna el valor de 1 que significa conectado 
                        
                        tiempoInicioSesion = time.time() # Guarda en la variable el tiempo de inicio de sesión del usuario conectado
                        
                        identificadorDelSocket = self.socket.fileno() # Guarda el número identificador del socket con que se comunica el servidor con el cliente en específico
                        
                        """
                        Guardad en la variable el nombre de usuario conectado más el identificador del socket de ese usuario separados por un espacio
                        
                        """
                        usuarioMasIndentificadorSocket = nombreUsuario + " " + str(identificadorDelSocket)
                        
                        bloqueo.acquire() #Bloquea el hilo
                        listaUsuariosMasIndentificadorSocket.append(usuarioMasIndentificadorSocket) #Guarda un registro nuevo en la lista
                        bloqueo.release()#Libera el hilo
                
            while True: #Ciclo que verifica el comando con la solicitud del cliente, según el comado el servidor ejecuta la acción correspondiente

                comando = str(self.socket.recv(1024), 'utf-8') # Se recibe del cliente cualquiera de los comandos válidos

                if "ENVIAR" in comando:# Verifica que en el comando enviado por el cliente esté la palabra ENVIAR               
                    contenido = comando.partition(" ") # Crea una tupla para separar la palabra ENVIAR de lo que contiene la varaible comando
                    receptorMasMensaje = contenido[2].partition(" ") # Se obtiene una nueva tupla que contiene el receptor y el mensaje                    
                    mensajeParaEnviar = nombreUsuario + " dice: " + receptorMasMensaje[2] # Se almacena en la variable la unión del usuario + "dice" + el mensaje.                  
                    receptor = receptorMasMensaje[0] # Se guarda el nombre del cliente que tiene que recibir el mensaje
                    banderaDeError = 1 # Se inicializa la variable con el valor 1, que significa que es un mensaje para un usuario que no está conectado
                    
                    for z in listaUsuariosMasIndentificadorSocket: # Ciclo for que recorre la lista que contiene los usuarios e identificadores de socket actualmente conectados
                        zi = z.partition(" ") # Crea una tupla temporal que contiene usuario más identificador
                        
                        if zi[0] == receptor: # Verifica que el cliente al cuál se le desea mandar el mensaje esté efectivamente en la lista de usuarios conectados activamente  
                            identificadorDelReceptor = int(zi[2]) # Se obtiene el identificador del socket del usuario al que se le desea mandar el mensaje
                            banderaDeError = 0 # se asigna cero ya que anteriormente se le había dado el valor 1 asumiendo por defecto que no estaba conectado el usuario al cuál se le desea enviar el mensaje
                            bloqueo.acquire() #Bloquea el hilo
                            colaParaEnviar[identificadorDelReceptor].put(mensajeParaEnviar)# Se agrega un nuevo elemento a la cola de mensajes que el servidor debe restrasmitir según corresponda
                            bloqueo.release()#Libera el hilo
                            
                    if banderaDeError == 1:
                        mensajeRespuesta = "Usuario desconectado. No se puede entregar el mensaje"# Se almacena en la variable el mensaje de que no se puede enviar porque está desconectado
                    else:
                        mensajeRespuesta = "mensaje enviado"#Se almacena en la variable el valor "mensaje enviado"
                    self.socket.send(bytes(mensajeRespuesta, 'utf-8'))#Se le notifica al cliente que el mensaje fue enviado.
                
                elif "EMITIR USUARIOS" in comando:#Condicional que verifica si el comando es "EMITIR USUARIOS"
                    contenido = comando.split(" ") #Divide la cadena que contiene comando y guarda el resulta en una lista denominada contenido
                    listaReceptores = [] #Lista que va contener los psobles receptores del mensaje que se desea emitir.
                    bandera = 0
                    mensajeParaEnviar = nombreUsuario + ":" #Se inicializa la variable con valor del nombre de usuario que está emitiendo el mensaje
                    
                    for i, palabra in enumerate(contenido): #Ciclo que recorre cada elemento según la cantidad de elmentos que tenga la lista contenido.
                        if ( i != 0 or i != 1): #Condicional que verifica que no sea el elemento 0 o 1 de la lista
                            if palabra != "mensaje" and bandera == 0: #Condicional que verifica que el valor de palabra no sea "mensaje" y además que el valor de bandera sea igual 0                           
                                listaReceptores.append(palabra) #Si se cumplen los dos anteriores condicionales significa que palabras contiene el valor del nombre de un usuario y lo guarda en la lista
                            elif palabra == "mensaje": #Verifica si palabra tiene el valor de "mensaje" para aumentar el valor de i en uno
                                i = i + 1 #aumenta el valor de i en 1
                                bandera = 1 #asigna el valor de 1 a la bandera
                            elif bandera == 1: #Condicional que verifica que ya palabra tiene el valor del mensaje que se desea trasmitir
                                mensajeParaEnviar = mensajeParaEnviar + " " + palabra #Se le concatena el valor de la variable palabra, que sería el mensaje a enviar
                                
                    for p in listaReceptores:#Se recorre la lista de receptores para comparar con los usuarios conectados para enviar el mensaje
                        print (p)
                        banderaDeError = 1# Se inicializa la variable con el valor 1, que indicaría posteriormente que alguno de los recptores no está conectado
                        for z in listaUsuariosMasIndentificadorSocket: #Se recorre la lista de usuarios más indentificador de socket para comparar con cada elemento de la lista de receptores 
                            zi = z.partition(" ") #Separa cada elemento de la lista para guardar usuario más identificador en zi
                            if p == zi[0]: #Compara si p que un posible recptor es igual a elemento 0 de zi que sería un usuario conectado
                                identificadorDelReceptor = int(zi[2]) #Extra el identificador del usuario
                                print (identificadorDelReceptor)
                                banderaDeError = 0 #Pone la bandera en 0 para indicar que es un usuario válido
                                bloqueo.acquire()#Bloquea el hilo
                                colaParaEnviar[identificadorDelReceptor].put(mensajeParaEnviar)# Se agrega un nuevo elemento a la cola de mensajes que el servidor debe restrasmitir según corresponda
                                bloqueo.release()#Libera el hilo
                                
                    if banderaDeError == 1: #Verifica si la variable trae el valor de 1 es que en la lista receptores había un usuario que no estaba conectado 
                        mensajeRespuesta = "No se pudo trasmitir el mensaje a todos los destinatarios, alguno de los usuarios estaba desconectado" #Sen indica que no se pudo enviar el mensaje
                        self.socket.send(bytes(mensajeRespuesta, 'utf-8')) #Se le reporta al cliente la acción 
                    else:
                        mensajeRespuesta = "mensaje transmitido" # Se confirma que si se retransmitió el mensaje a todos
                        self.socket.send(bytes(mensajeRespuesta, 'utf-8')) #Se le reporta al cliente la acción
                        
                elif comando == "CONECTADOS": #Condicional que verifica si el comando es "CONECTADOS"
                    conectados = " " #Inicializa la variable con un espacio en blanco
                    for p in usuariosActuales: #Ciclo que recorre la lista de usuarios actuales
                        if p != nombreUsuario: #Se excluye el cliente que realizó la consulta
                            conectados = conectados + p + " " #Guarda en la variable conectados cada uno de los nombres de los usuarios que están conectados
                    if conectados == " ": #Verifica si conectados tiene aun el espacio en blanco para indicar que nadie está conecatdo además de él
                        conectados = "Nadie está conectado de momento...solo usted" #Guarda ese valor en la variable conectados
                        self.socket.send(bytes(conectados,'utf-8')) #Reporta al cliente
                    else: #Significa que se habían otros conectados
                        self.socket.send(bytes(conectados,'utf-8')) #Reporta al cliente
                        
                elif "EMITIR MENSAJE" in comando: #Verifica que la variable comando tenga "EMITIR MENSAJE"
                    #En seguida las instrucciones que extraen el mensaje que se tiene que enviar a todos los usuarios
                    mensaje = comando.partition(" ")
                    mensajeFinal = mensaje[2].partition(" ")
                    #Finalmente se guarda en la variable msg el mensaje que se la va a dar a los usuarios
                    msg = nombreUsuario + "dice: " + mensajeFinal[2]

                    #Se coloca en la cola de mensajes el mensaje a cada usuario para enviar
                    bloqueo.acquire()#Bloquea el hilo
                    for  q in colaParaEnviar.values():
                        q.put(msg)
                    bloqueo.release()#Libera el hilo
                    
                    mensajeRespuesta = "transmitido"  #Mensaje para reportar al cliente    
                    self.socket.send(bytes(mensajeRespuesta, 'utf-8')) #Se envía el mensaje de reporte al cliente
                    
                elif comando == "DESCONECTAR":
                    usuariosActuales.remove(nombreUsuario)
                    datosDeDesconectados = nombreUsuario

                    print (datosDeDesconectados, "eliminado")
                    mensajeRespuesta = "desconectado"
                    self.socket.send(bytes(mensajeRespuesta, 'utf-8'))
                    print ("Hilo desconectado para "+ip+": "+str(puerto))
                    indetificadorDelSocket = self.socket.fileno()
                    bloqueo.acquire()
                    del colaParaEnviar[indetificadorDelSocket]
                    listaUsuariosMasIndentificadorSocket.remove(usuarioMasIndentificadorSocket)
                    bloqueo.release()
                    sys.exit()
                else:
                    error = "Comando inválido. Por favor digite un comando válido: "
                    self.socket.send(bytes(error, 'utf-8'))
                    
        #bloqueo.acquire()    
        #usuariosActuales.remove(nombreUsuario) 
        #bloqueo.release()
        
        #datosDeDesconectados = nombreUsuario + " " + str(tiempoInicioSesion)
        
        #lock.acquire()
        #usuariosDesconectados.append(datosDeDesconectados)
        #lock.release()
        #print (datosDeDesconectados , "eliminado")
        #print ("desconectado")
        #sys.exit()
"""
Clase construida, denominada HiloClienteLectura. Esta clase lo que hace es manejar un hilo exclusivo en el programa servidor para retrasmitir los mensajes del chat
que un cliente específico, envía a otro cliente.

Como es una clase construida que va manejar hilos, entonces hereda de la clase Threand de Python.

Al momento de crear un ejemplar de esta clase en el programa, la clase recibe como parametro on objeto socket.

"""

class HiloClienteLectura(Thread):
    #A continuación el método cosntructor de la clase
    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock
        
        print ("Se inició un nuevo hilo para la confiabilidad del chat y trasmisión de mensajes")

    #A continuación el método run de la clase
    
    def run(self):
         
         
         socketServidor2.listen(1)
         
         (conexionSocketConCliente2, (ip,puerto)) = socketServidor2.accept()
         
         mensajeBienvenida = "Hola bienvenido al chat..."
         
         conexionSocketConCliente2.send(bytes(mensajeBienvenida, 'utf-8'))
         
         mensajeChatParaEnviar = "inicial"
         
         print ("El identificador del socket creado para el cliente es este: ", self.sock.fileno())
         
         while True:
             try:

                 mensajeChatParaEnviar = colaParaEnviar[self.sock.fileno()].get(False)
                 conexionSocketConCliente2.send(bytes(mensajeChatParaEnviar, 'utf-8'))
                 
             except queue.Empty:

                 mensajeChatParaEnviar = "ninguno"
                 time.sleep(2)
                 
             except KeyError as e:
                pass

#Inicio de programa principal

"""
threading.Lock()
Una función fábrica que devuelve un objeto cerrojo primitivo nuevo.
Tras ser adquirido por un hilo, los posteriores intentos de adquirirlo bloquearán su ejecución hasta que sea liberado. Cualquier hilo puede liberarlo.

"""
bloqueo = threading.Lock()

global comando

comando = ""


colaParaEnviar = {}

IP = '127.0.0.1' #Dirección IP del servidor

PUERTO_ESCUCHA1 = int(5000)

PUERTO_ESCUCHA2 = int(125)

#TAMANO_BUFER = 20

usuariosActuales = [] #Lista que almacena usuarios actuales conectados
listaUsuariosMasIndentificadorSocket = []

 
socketServidor1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketServidor1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


socketServidor1.bind(('127.0.0.1', PUERTO_ESCUCHA1))

socketServidor2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketServidor2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socketServidor2.bind(("127.0.0.1", PUERTO_ESCUCHA2))
         

#hilos = []
 
while True:
    

    """La siguiente instrucción indica al sistema operativo que el programa cliente está listos para admitir conexiones.
        El número 6 de parámetro indica cuantos clientes puede tener encolados en espera simultáneamente.

        Este número no debería ser grande, puesto que es el número máximo de clientes que quedarán encolados desde que se acepta
        un cliente hasta que estamos dispuestos a aceptar el siguiente.
        
        Si el código está bien hecho, este tiempo debería ser realmente pequeño, ya que al conectarse un cliente,
        deberíamos lanzar un hilo para atenderlo y entrar inmediatamente a la espera de otro cliente.
    """
  
    socketServidor1.listen(6)
    
    print ("El servidor está listo, esperando por conexiones entrantes...")
    
    (conexionSocketConCliente, (ip,puerto)) = socketServidor1.accept()

    
    q = queue.Queue()

    
    bloqueo.acquire()
      
    colaParaEnviar[conexionSocketConCliente.fileno()] = q
    
    bloqueo.release()
    
           
    print ("Se creará un hilo con el socket identificado con el número: " , conexionSocketConCliente.fileno())
    
    hilonuevo1 = HiloCliente(conexionSocketConCliente,ip,puerto)
    hilonuevo1.daemon = True
    hilonuevo1.start()
    
    hilonuevo2 = HiloClienteLectura(conexionSocketConCliente)
    hilonuevo2.daemon = True
    hilonuevo2.start()
