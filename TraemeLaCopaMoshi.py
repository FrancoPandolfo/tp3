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

	archivo.close()

else:
	print('archivo incorrecto')
	sys.exit()

while True:
	
	text = input("entrada:")

	cadena = text.split(' ')

	if cadena[0] == 'ir':
		cadena[1] = cadena[1][:-1]
		camino = lib.camino_minimo(grafoPesado,cadena[1],cadena[2])
		for i in range(0,len(camino[0])-1):
			print(camino[0][i],'-> ', end='')
		print(camino[0][len(camino[0])-1])
		print('Costo total: ', camino[1])

	elif cadena[0] == 'viaje':
		cadena[1] = cadena[1][:-1]

		if cadena[1] == 'optimo':
			print(lib.viajante(grafoPesado,cadena[2]))

		elif cadena[1] == 'aproximado':
			camino = lib.viajante_aproximado(grafoPesado,cadena[2])
			for i in range(0,len(camino[0])-1):
				print(camino[0][i],'-> ', end='')
			print(camino[0][len(camino[0])-1])
			print('Costo total: ', camino[1])

		else:
			print('comando incorrecto')
			sys.exit()

	elif cadena[0] == 'itinerario':
		'''if os.path.isfile(sys.argv[1]) == True:
			archivo = open(cadena[1], 'r')
			with open(cadena[1]) as archivo:  
   				for cnt, lectura in enumerate(fp):
					linea = lectura.split(',')
					grafoDirigido.AgregarVertice(linea1[0])'''

		lib.orden_topologico(grafoDirigido)



	elif cadena[0] == 'reducir_caminos':
		arbol = lib.arbol_tendido_minimo(grafoPesado)
		visitado = []
		file = open(cadena[1],'w')

		file.write("%s\n" % ( str(len(arbol.dic)) ) )
		for v in arbol.dic:
			file.write("%s\n" % (v) )
		file.write("%s\n" % ( str(arbol.CantidadAristas()) ) )
		for v in arbol.dic:
			visitado.append(v)
			for w in arbol.VerVecinos(v):
				if v == w:
					continue
				if w not in visitado:
					file.write("%s,%s,%s\n" % (v, w, str(arbol.VerPeso(v,w))) )
		file.close()
		print(arbol.PesoTotal())			


	else:
		print('comando incorrecto')
		sys.exit()