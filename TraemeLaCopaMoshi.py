import os.path
import sys
import lib
from grafoPeso import grafoPeso
from grafoDir import grafoDir

grafoPesado = grafoPeso({})
grafoDirigido = grafoDir({})

if os.path.isfile(sys.argv[1]) == True:
	archivo = open(sys.argv[1], 'r')
	cantidadV = int(archivo.readline())
	for i in range(0,cantidadV):
		lectura1 = archivo.readline()
		linea1 = lectura1.split(',')
		grafoPesado.AgregarVertice(linea1[0])
		grafoDirigido.AgregarVertice(linea1[0])

	cantidadA = int(archivo.readline())
	for j in range(0,cantidadA):
		lectura2 = archivo.readline()
		linea2 = lectura2.split(',')
		grafoPesado.AgregarArista( (linea2[0],linea2[1],int(linea2[2])) )
		grafoDirigido.AgregarArista((linea2[0],linea2[1]))

	archivo.closed
else:
	print('archivo incorrecto')
	sys.exit()

while True:
	
	text = input("entrada:")

	cadena = text.split(' ')

	if cadena[0] == 'ir':
		cadena[1] = cadena[1][:-1]
		lib.camino_minimo(grafoPesado,cadena[1],cadena[2])

	elif cadena[0] == 'viaje':
		cadena[1] = cadena[1][:-1]
		if cadena[1] == 'optimo':
			lib.viajante(grafoPesado,cadena[2])
		elif cadena[1] == 'aproximado':
			lib.viajante_aproximado(grafoPesado,cadena[2])
		else:
			print('comando incorrecto')
			sys.exit()

	elif cadena[0] == 'itinerario':
		lib.orden_topologico(grafoDirigido)

	elif cadena[0] == 'reducir_caminos':
		lib.arbol_tendido_minimo(grafoPesado)

	else:
		print('comando incorrecto')
		sys.exit()