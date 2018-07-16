import os.path
import sys
import lib
from grafoPeso import grafoPeso
from grafoDir import grafoDir

grafoPesado = grafoPeso({})
grafoDirigido = grafoDir({})

coordenadas = {}

if len(sys.argv) < 3:
	print('faltan parametros')
	sys.exit()

if os.path.isfile(sys.argv[1]) == True:

	archivo = open(sys.argv[1], 'r')
	cantidadV = int(archivo.readline())
	for i in range(0,cantidadV):
		lectura1 = archivo.readline()
		lectura1 = lectura1[:-1]
		linea1 = lectura1.split(',')
		grafoPesado.AgregarVertice(linea1[0])
		grafoDirigido.AgregarVertice(linea1[0])
		coordenadas[linea1[0]] = (linea1[2],linea1[1])

	cantidadA = int(archivo.readline())
	for j in range(0,cantidadA):
		lectura2 = archivo.readline()
		linea2 = lectura2.split(',')
		grafoPesado.AgregarArista( (linea2[0],linea2[1],int(linea2[2])) )
		grafoDirigido.AgregarArista((linea2[0],linea2[1]))
		grafoDirigido.AgregarArista((linea2[1],linea2[0]))

	archivo.close()
else:
	print('archivo incorrecto')
	sys.exit()

while True:
	
	text = input("entrada:")
	if len(text) > 1:
		text[-1]
	cadena = text.split(' ')
	print(text)

	if cadena[0] == 'ir':
		cadena[1] = cadena[1][:-1]
		camino = lib.camino_minimo(grafoPesado,cadena[1],cadena[2])
		for i in range(0,len(camino[0])-1):
			print(camino[0][i],'-> ', end='')
		print(camino[0][len(camino[0])-1])
		print('Costo total:', camino[1])
		archivo = sys.argv[2]
		lib.armar_archivo1(archivo,camino,coordenadas)

	elif cadena[0] == 'viaje':
		cadena[1] = cadena[1][:-1]

		if cadena[1] == 'optimo':
			camino = lib.viajante(grafoPesado,cadena[2])
			for i in range(0,len(camino[0])-1):
				print(camino[0][i],'-> ', end='')
			print(camino[0][len(camino[0])-1])
			print('Costo total:', camino[1])
			archivo = sys.argv[2]
			lib.armar_archivo1(archivo,camino,coordenadas)

		elif cadena[1] == 'aproximado':
			camino = lib.viajante_aproximado(grafoPesado,cadena[2])
			for i in range(0,len(camino[0])-1):
				print(camino[0][i],'-> ', end='')
			print(camino[0][len(camino[0])-1])
			print('Costo total:', camino[1])
			archivo = sys.argv[2]
			lib.armar_archivo1(archivo,camino,coordenadas)

		else:
			print('comando incorrecto')
			sys.exit()

	elif cadena[0] == 'itinerario':
		if os.path.isfile(cadena[1]) == True:
   			archivo = open(cadena[1], 'r')
   			lista = []
   			for line in archivo:
   				line=line[:-1]
   				linea = line.split(',')
   				lista.append((linea[0],linea[1]))


		if os.path.isfile(cadena[1]) == False:
			print('archivo incorrecto')
			sys.exit()

		archivo.close()

		camino = lib.orden_topologico(grafoDirigido,lista)
		if camino == None:
			print(None)
		else:
			for i in range(0,len(camino)-1):
				print(camino[i],'-> ', end='')
			print(camino[len(camino)-1])
			archivo = sys.argv[2]
			lib.armar_archivo2(archivo,camino,coordenadas)
			


	elif cadena[0] == 'reducir_caminos':
		arbol = lib.arbol_tendido_minimo(grafoPesado)
		visitado = []
		file = open(cadena[1],'w')

		file.write("%s\n" % ( str(len(arbol.dic)) ) )
		for v in arbol.dic:
			coord = coordenadas[v]
			file.write("%s,%s,%s\n" % (v,coord[1],coord[0]) )
		file.write("%s\n" % ( str(arbol.CantidadAristas()) ) )
		for v in arbol.dic:
			visitado.append(v)
			for w in arbol.VerVecinos(v):
				if v == w:
					continue
				if w not in visitado:
					file.write("%s,%s,%s\n" % (v, w, str(arbol.VerPeso(v,w))) )
		file.close()
		print('Peso total:',arbol.PesoTotal())			


	else:
		print('comando incorrecto')
		sys.exit()