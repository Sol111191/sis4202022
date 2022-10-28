# -*- coding: utf-8 -*-
"""misioneroYcanibal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13orqHJjkmDkvps0k-_xrpSyBqD-dG-Es

Para este ejercio se usara la busqueda en anchura para poder resolver el problema, primero se creara la clase estado con sus metodos siguentes init, atr, es verificacion de estado valido, estado final, eq , hash, 
en esta primera parte se inicializaran lo atributos del objeto estado, posterior a eso se verificacaran las restricciones para los misioneros y canibales de ambos lado , y el objetivo final que es pasar a todos los misioneros y canibales al otro lado del rio sin quedar afectados ninguno.
Se construira el metodo que genere las siguentes acciones posibles y creando la copya de cada estado y ademas empezara po el bote si el bote es = 0 enronces podra moverse de la izquerda hacia la derecha y para volver del viaje el bote retornara siempre con un canibal o misionero para ir de la derecha hacia la izquerda hasta que ya no queden mas misioneros o canibales en el lado izquierdo 
eso se ara con una cola que ira almacenando los viajes posibles que son 11 acciones
"""

from copy import deepcopy #una copia profunda construye un muevo objeto y luego recursivamente inserta copias d elos objetos encontrados 


#posibilidades que tiene el numero de canibales 
#y misioneros para avanzar en esa accion  en el barco 
POSIBILIDADES = [[1,1],[0,2],[2,0],[0,1],[1,0]]

#clase Estado
class Estado():
	# metodo que inicializa los atributos del objeto y sus argumentos que creamos
	def __init__(self, izquierda, barco, derecha): 
		self.izquierda=izquierda; # El parametro self hace referencia al obgeto instanciado de esa clase sobre el cual se esta invocando dicho metodo
		self.barco = barco;
		self.derecha=derecha;
		self.anterior = None
		#metodo que devuelve en cadena e imprime los misioneros, canibales y el barco
	def __str__(self):
		return("({},{}) - ({},{}) - {}".format(self.izquierda[0],self.izquierda[1], self.derecha[0],self.derecha[1], self.barco))
	
	# Metodo para Comprobar restricciones
	def esVerificacionDeEstadoValido(self):	
		#Para ambos lados, los misioneros presentes en el lado no pueden ser superados en número por caníbales.
		if(0 < self.izquierda[0] < self.izquierda[1] or 0 < self.derecha[0] < self.derecha[1]):
			return False	
		
		#No se transportan más misioneros/caníbales de los que existen en un lado
		if(self.izquierda[0]<0 or self.izquierda[1]<0 or self.derecha[0]<0 or self.derecha[1]<0):
			return False
		
		return True
		#python llama automaticamente al metodo  --eq-- de una clase cuando  usa el operador == para 
		#comparar las instancias de la clase , es decir los valores de las matrices (izquerda-derecha-barco)
	def __eq__(self, otro):   
		return (self.izquierda[0]==otro.izquierda[0] and self.izquierda[1] == otro.izquierda[1] and self.derecha[0]==otro.derecha[0] and self.derecha[1]==otro.derecha[1] and self.barco==otro.barco)
		# metodo --hash-- compara las instancias de las clases cuando alla una diferencia dentro de los valores de las matrices
	def __hash__(self):   
		return hash((self.izquierda[0],self.izquierda[1],self.barco,self.derecha[0],self.derecha[1]))
	#metodo que devuelve texto en tipo string e imprime el rrecorrido de misioneros, canibales y el barco
	def __str__(self):
		return("({},{}) - ({},{}) - {}".format(self.izquierda[0],self.izquierda[1],self.derecha[0],self.derecha[1],self.barco))
	
	#Mueve con éxito a todos los misioneros y caníbales del lado izquierdo al derecho
	def EstadoFinal(self):
		return(self.izquierda[0]==0 and self.izquierda[1]==0)

# Metodo para generar los siguentes estados 
def SiguentesEstados(actual):
	nodos=[]
	# tratamos de generar todos los estados posibles y luego los filtramos
  # estados que son válidos
	for accion in POSIBILIDADES:
		
		siguenteEstado = deepcopy(actual)  #construye un nuevo objeto y luego recursivamente inserta copias en el de los objetos encontrados en el original
		siguenteEstado.anterior=actual	  # el estado siguente instancia a la variable anterior y este toma el estado actual 
		
		#El barco estará en el lado opuesto.
		siguenteEstado.barco = 1-actual.barco
		
		#De izquierda a derecha
		if(actual.barco==0):

			#Aumentar el número en el lado derecho
			siguenteEstado.derecha[0]+=accion[0]
			siguenteEstado.derecha[1]+=accion[1]
			
			#Disminuye el número en el lado izquierdo
			siguenteEstado.izquierda[0]-=accion[0]
			siguenteEstado.izquierda[1]-=accion[1]
		
		#De derecha a izquierda
		elif(actual.barco==1):
			
			#Disminuye el número en el lado derecho
			siguenteEstado.derecha[0]-=accion[0]
			siguenteEstado.derecha[1]-=accion[1]
			
			#Aumentar el número en el lado izquierdo
			siguenteEstado.izquierda[0]+=accion[0]
			siguenteEstado.izquierda[1]+=accion[1]
		
		if siguenteEstado.esVerificacionDeEstadoValido():   # volevemos a verificar si es estado es valido 
			nodos.append(siguenteEstado)		# y agregamos al nodo el estado actual

	return nodos  #retornamos al nodo

# metodo que hace la busqueda por anchura 
def bfs(origen):
	
	if origen.EstadoFinal():
		return origen
	
	visitado = set()
	cola = [origen]

	while cola:		#mientras aya en la cola 
		estado = cola.pop()   #la variable estado le ira quitando de la cola con (pop)
		if estado.EstadoFinal():
			return estado
		
		visitado.add(estado)
		
		for hijo in SiguentesEstados(estado):
			if hijo in visitado:
				continue
				#si no estubo alla 
			if hijo not in cola: # not in devuelve true si un elemento no se encuentra dentro de otro ,
														# en este caso el hijo  de la cola establecida 
				cola.append(hijo)		#la cola ira almacenado los valores de hijo mediante el metodo append dentro de la cola

def main():
	initial_estado = Estado([3,3],0,[0,0])
	estado = bfs(initial_estado)
	
	camino=[]
	while  estado:
		camino.append(estado)
		estado = estado.anterior
		#empieza por el final 
	camino=camino[::-1]
	
	print("")
	print("Problema de misioneros y caníbales resuelto usando Breadth First Search (busqueda por anchura)")
	print("M - Misioneros C - Caníbales b - Barco")
	print("")

#imprimir resultado del estado
	for estado in camino:
		
		if estado.barco: # estado del barco si es verdadero = 1 o falso = 0  (barco a la derecha o iquierda)
			print("""{:3} |         b| {:3}\n{:3} |          | {:3}""".format("C"*estado.izquierda[1], "C"*estado.derecha[1], "M"*estado.izquierda[0], "M"*estado.derecha[0])) # se muestra los viajes de los M y C 
		else: 
			print("""{:3} |b         | {:3}\n{:3} |          | {:3}""".format("C"*estado.izquierda[1], "C"*estado.derecha[1], "M"*estado.izquierda[0], "M"*estado.derecha[0])) 
		print("-------------------------") #visualizar mejor con grafica
		print("")
		print("-------------------------")

if __name__ == "__main__": #la variable __name__ se establecera como __main__ si el modulo que se esta ejecutando es el programa principal
	main()