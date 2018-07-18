import heapq
import queue
import random
import math
import itertools
import os.path
from collections import OrderedDict
from grafoPeso import grafoPeso
from grafoDir import grafoDir

def buscar_pos(dic,vertice):
	cont = 0
	for v in dic:
		if v == vertice:
			break
		cont += 1
	return cont

def buscar_vertice(dic,pos):
	cont = 0
	for v in dic:
		if cont == pos:
			return v
		cont += 1

def viajante_floyd(grafo,origen):
	w, h = len(grafo.dic), len(grafo.dic);
	dist = [[math.inf for x in range(w)] for y in range(h)]
	for i in range(0,h):
		dist[i][i] = 0
	posV = 0
	for v in grafo.dic:
		for w in grafo.dic[v]:
			posW = buscar_pos(grafo.dic,w)
			dist[posV][posW] = grafo.VerPeso(v,w)
		posV += 1
	for k in range(0,h):
		for i in range(0,h):
			for j in range(0,h):
				if dist[i][j] > dist[i][k] + dist[k][j]:
					dist[i][j] = dist[i][k] + dist[k][j]
	return dist


def encontrar_minimo(grafo,camino,costoMinimo):
	for i in range(0,len(camino)):
		if i+1 < len(camino):
			actual = camino[i]
			siguiente = camino[i+1]
			costoMinimo += grafo.VerPeso(actual,siguiente)
		else:
			continue
	return costoMinimo

distancia_optima = -1
camino_optimo = []
def encontrar_caminos_aux(grafo,origen,vertices, inicio):
	global distancia_optima, camino_optimo
	if inicio >= len(vertices):
		distancia_actual = 0
		distancia_actual = calcular_distancia(grafo,origen,vertices,distancia_actual)
		if distancia_optima == -1 or distancia_actual < distancia_optima:
			distancia_optima = distancia_actual
			camino_optimo = vertices[:]
	else:
		for i in range(inicio,len(vertices)):
			vertices[i], vertices[inicio] = vertices[inicio], vertices[i]
			actual = vertices[0]
			distancia_aux = 0
			for j in range(1,inicio):
				siguiente = vertices[j]
				distancia_aux += grafo.VerPeso(actual,siguiente)
				actual = siguiente
			if distancia_optima == -1 or distancia_aux < distancia_optima:
				encontrar_caminos_aux(grafo,origen,vertices, inicio +1)
				vertices[inicio], vertices[i] = vertices[i], vertices[inicio]
			else:
				break

def encontrar_caminos(grafo,origen, vertices):
	distancia_optima = -1
	camino_optimo = []
	encontrar_caminos_aux(grafo,origen, vertices,0)

def encontrar_caminos_aux2(grafo,vertices,orden_actual, suma_actual, vertices_restantes):
	global distancia_optima, camino_optimo
	if len(orden_actual) == len(vertices):
		orden_final = orden_actual[:]
		orden_final.append(orden_actual[0])
		suma_final = suma_actual
		suma_final += grafo.VerPeso(orden_actual[len(orden_actual) -1],orden_actual[0])
		if suma_final < distancia_optima or distancia_optima == -1:
			distancia_optima = suma_final
			camino_optimo = orden_final
			return

	for i in vertices_restantes:
		vertices_aux = vertices_restantes[:]
		vertices_aux.remove(i)
		orden_copia = orden_actual[:]
		orden_copia.append(i)
		suma_actual_copia = suma_actual
		if len(orden_copia) > 1:
			suma_actual_copia += grafo.VerPeso(orden_copia[len(orden_copia)-2], i)
		if suma_actual_copia < distancia_optima or distancia_optima == -1:
			encontrar_caminos_aux2(grafo,vertices,orden_copia,suma_actual_copia,vertices_aux)


def encontrar_caminos2(grafo,origen, vertices):
	distancia_optima = -1
	camino_optimo = []
	orden_actual = []
	suma_actual = 0
	encontrar_caminos_aux2(grafo, vertices,orden_actual,suma_actual,vertices )

def arreglar_camino(origen):
	global camino_optimo
	lar = len(camino_optimo)
	nuevo_camino = []
	nuevo_camino.append(origen)
	for i in range(0,lar):
		if camino_optimo[i] == origen:
			cont1 = i + 1
			break

	for j in range(cont1,len(camino_optimo)):
		nuevo_camino.append(camino_optimo[j])

	for k in range(1,cont1):
		nuevo_camino.append(camino_optimo[k])

	nuevo_camino.reverse()
	#nuevo_camino[lar-4],nuevo_camino[lar-7] = nuevo_camino[lar-7], nuevo_camino[lar-4]
	#nuevo_camino[lar-5],nuevo_camino[lar-6] = nuevo_camino[lar-6], nuevo_camino[lar-5]
	return nuevo_camino


def viajante(grafo,origen):
	global camino_optimo, distancia_optima
	camino_optimo = []
	distancia_optima = -1
	vertices = list(grafo.dic.keys())
	caminos = []
	encontrar_caminos2(grafo,origen,vertices)
	camino_optimo = arreglar_camino(origen)
	return camino_optimo, distancia_optima

'''def viajante(grafo,origen):
	global camino_optimo, distancia_optima
	camino_optimo = []
	distancia_optima = -1
	dic = grafo.dic.copy()
	del dic[origen]
	vertices = list(dic.keys())
	caminos = []
	encontrar_caminos(grafo,origen,vertices)
	camino_optimo.insert(0,origen)
	camino_optimo.append(origen)
	#camino_optimo = arreglar_camino(origen)
	return camino_optimo, distancia_optima'''

def backtrack(grafo,vertices,caminos,visitado,pila,u):
	if len(pila) == len(grafo.dic):
		caminos.append(pila[:])
		pila = []
	visitado.append(u)
	for w in grafo.VerVecinos(u):
		if w not in visitado:
			pila.append(w)
			backtrack(grafo,vertices,caminos,visitado,pila,w)
	visitado.remove(u)

def back(grafo,vertices,caminos):
	visitado = []
	pila = []
	for u in grafo.dic:
		pila.append(u)
		backtrack(grafo,vertices,caminos,visitado,pila,u)
	return caminos

'''def viajante(grafo,origen):
	dic = grafo.dic.copy()
	del dic[origen]
	vertices = list(dic.keys())
	caminos = []
	print(back(grafo,vertices,caminos))
	#camino_optimo.insert(0,origen)
	#camino_optimo.append(origen)
	#print(caminos)
	#return camino_optimo, distancia_optima'''

'''def tsp1(grafo,vertices,l,largo,costo):
	n = len(vertices)
	if l == n:
		costo = min(costo,largo+grafo.VerPeso(vertices[n],vertices[0]))
	else:
		for i in range(l+1,n):
			vertices[l+1], vertices[i] = vertices[i], vertices[l+1]
			nuevoLargo = largo + grafo.VerPeso(vertices[l],vertices[l+1])
			if nuevoLargo >= costo:
				break
			else:
				costo = min(costo,tsp1(vertices,l+1,nuevoLargo,costo))
				vertices[l+1], vertices[i] = vertices[i], vertices[l+1]
	return costo

def viajante(grafo,origen):
	global distancia_optima
	distancia_optima = -1
	dic = grafo.dic.copy()
	del dic[origen]
	vertices = list(dic.keys())
	caminos = []
	costo = -1
	costo = tsp1(grafo,vertices,0,0,costo)
	print(costo)'''
	#camino_optimo.insert(0,origen)
	#camino_optimo.append(origen)
	#print(caminos)
	#return camino_optimo, distancia_optima

"""	Arma los posibles recorridos desde y hacia el origen """
def recorrido_armar(grafo, origen):
	dic = grafo.dic.copy()
	del dic[origen]
	lista = list(dic.keys())
	return lista

def min(a, b):
	if a < b:
		return a 
	return b

def swap(a, b):
	aux = a 
	a = b
	b = aux

def distancia(grafo, a, b):
	return grafo.VerPeso(a, b)

def tsp(grafo, A, l, lengthSoFar, minCost):
	n = len(A)
	if l == n-1:
		minCost = min(minCost, lengthSoFar + distancia(grafo, A[n-1], A[0]))
	else:
		for i in range(l, n):
			A[i], A[l] = A[l], A[i]
			#swap(A[l + 1], A[i])
			newLength = lengthSoFar + distancia(grafo, A[l], A[l + 1])
			if newLength < minCost:
				minCost = min(minCost, tsp(grafo, A, l + 1, newLength, minCost))
				#swap(A[l + 1], A[i])
				A[l], A[i] = A[i], A[l]
			else:
				continue
	return minCost

"""	Devuelve el menor recorrido desde y hacia el origen """
'''def viajante(grafo, origen):
	recorrido = recorrido_armar(grafo, origen)
	minCost = math.inf
	minCost = tsp(grafo, recorrido, 0, 0, minCost)
	recorrido.insert(0, origen)
	recorrido.append(origen)
	return recorrido, minCost'''

def calcular_distancia(grafo,origen,vertices, distancia_actual):
	actual = vertices[0]
	for i in range(1,len(vertices)):
		siguiente = vertices[i]
		distancia_actual += grafo.VerPeso(actual,siguiente)
		actual = siguiente
	distancia_actual += grafo.VerPeso(origen,vertices[0])
	distancia_actual += grafo.VerPeso(origen,vertices[len(vertices)-1])
	return distancia_actual

def distancias(grafo,caminos,costos):
	for i in range(0,len(caminos)):
		actual = caminos[i][0]
		for j in range(1,len(caminos[i])):
			siguiente = caminos[i][j]
			costos[i] += grafo.VerPeso(actual,siguiente)
			actual = siguiente
	return costos

def menor_camino(costos,caminos,camino,costo):
	costo = costos[0]
	costo_actual = 0
	pos = 0
	for i in range(1,len(costos)):
		costo_actual = costos[i]
		if costo_actual < costo:
			costo = costo_actual
			pos = i
	camino = caminos[i]
	return camino, costo

def permutaciones_aux(grafo,dic, v,origen,i):
	camino = [v]
	visitado = {v}
	def search(i):
		global distancia_optima, camino_optimo
		sin_salida = True
		for w in dic[camino[-1]]:
			if w == origen:
				visitado.add(w)
			if w not in visitado:
				sin_salida = False
				visitado.add(w)
				camino.append(w)
				actual = camino[0]
				distancia_aux = 0
				for j in range(1,i):
					siguiente = camino[j]
					distancia_aux += grafo.VerPeso(actual,siguiente)
					actual = siguiente
				if distancia_optima == -1 or distancia_aux < distancia_optima:
					yield from search(i+1)
					camino.pop()
					visitado.remove(w)
				else:
					camino.pop()
					visitado.remove(w)
					search(i)
					break
		if sin_salida:
			distancia_actual = 0
			distancia_actual = calcular_distancia(grafo,origen,camino,distancia_actual)
			if distancia_optima == -1 or distancia_actual < distancia_optima:
				distancia_optima = distancia_actual
				camino_optimo = camino[:]
			yield list(camino)
	yield from search(i+1)

def permutaciones(grafo,dic,caminos,origen):
	distancia_optima = -1
	for v in dic:
		if v == origen:
			continue
		permutacion_actual = sorted(permutaciones_aux(grafo,dic,v,origen,0))
		for i in range(0,len(permutacion_actual)):
			caminos.append(permutacion_actual[i])
	return caminos

'''def viajante(grafo,origen):
	global camino_optimo, distancia_optima
	camino_optimo = []
	distancia_optima = -1
	dic = grafo.dic.copy()
	del dic[origen]
	vertices = list(dic.keys())
	#encontrar_caminos(grafo,origen,vertices)
	camino = []
	costo = 0
	caminos = []
	caminos = permutaciones(grafo,grafo.dic,caminos,origen)
	camino_optimo.insert(0,origen)
	camino_optimo.append(origen)
	costos = [0] * len(caminos)
	#costos = distancias(grafo,caminos,costos)
	#camino, costo = menor_camino(costos,caminos,camino,costo)
	return camino_optimo, distancia_optima'''


def viajante_aproximado_funcion(grafo,origen):
	visitado = []
	padre = {}
	dist = {}
	visitado.append(origen)
	heap = []
	heap2 = []
	padre[origen] = None
	dist[origen] = 0
	heapq.heappush(heap,origen)
	while len (heap) > 0:
		v = heapq.heappop(heap)
		contador = 0
		for w in grafo.VerVecinos(v):
			a = (grafo.VerPeso(v,w),v,w)
			heapq.heappush(heap2,a)
			contador += 1
		while len (heap2) > 0:
			u = heapq.heappop(heap2)
			contador -= 1
			if u[2] not in visitado:
				visitado.append(u[2])
				padre[u[2]] = v
				dist[u[2]] = dist[v] + u[0]
				heapq.heappush(heap,u[2])
				break
			else:
				continue
		for i in range(0,contador):
			heapq.heappop(heap2)
	return padre,dist

def viajante_aproximado(grafo,origen):
	padre, dist = viajante_aproximado_funcion(grafo, origen)
	viaje = []
	peso_total = 0
	for v in padre:
		viaje.append(v)
	vertice = list(padre.keys())[-1]
	viaje.append(origen)
	peso_total = dist[vertice] + grafo.VerPeso(vertice,origen)
	return viaje, peso_total

"""	Devuelve una lista con el camino mínimo, y la menor distancia desde
	el origen hacia el destino	"""
def dijkstra(grafo, origen):
	dist = {}
	padre = {}
	for v in grafo.MostrarVertices():
		dist[v] = math.inf
	dist[origen] = 0
	padre[origen] = None
	heap = []
	heapq.heappush(heap, (0, origen))
	while len(heap) > 0:
		peso, v = heapq.heappop(heap)
		for w in grafo.VerVecinos(v):
			if dist[v] + grafo.VerPeso(v, w) < dist[w]:
				dist[w] = dist[v] + grafo.VerPeso(v, w)
				padre[w] = v
				heapq.heappush(heap, (dist[w], w))
	return padre, dist

def armar_camino(padre, destino):
	aux = destino
	camino = []
	while aux:
		camino.append(aux)
		aux = padre[aux]
	camino.reverse()
	return camino

def camino_minimo(grafo, origen, destino):
	padre, dist = dijkstra(grafo, origen)
	return armar_camino(padre, destino), dist[destino]

def orden_topologico(grafo,lista):
	grado = {}
	for u in grafo.dic:
		grado[u] = 0
	'''for m in grafo.dic:
		for w in grafo.VerVecinos(m):
			grado[w] += 1'''
	aux = []
	g = 0
	for x in lista:
		aux.append(x[0])
	aux = OrderedDict((x, True) for x in aux).keys()
	for y in aux:
		g += 1
		grado[y] += g
	for tupla in lista:
		if grado[tupla[1]] <= grado[tupla[0]]:
			grado[tupla[1]] = grado[tupla[0]] + 1
	resul = []
	cola = queue.Queue()
	for n in grafo.dic:
		if grado[n] == 0:
			cola.put(n)
	while not cola.empty():
		x = cola.get()
		resul.append(x)
		for v in grafo.VerVecinos(x):
			grado[v] -= 1
			if grado[v] == 0:
				cola.put(v)
	if len(resul) != len(grafo.dic):
		return None
	else:
		return resul

def arbol_tendido_minimo(grafo):
	inicio = random.choice(list(grafo.dic.keys()))
	visitado = []
	visitado.append(inicio)
	heap = []
	for w in grafo.VerVecinos(inicio):
		arista1 = (grafo.VerPeso(inicio,w),inicio,w)
		heapq.heappush(heap,arista1)
	arbol = grafoPeso({})
	for x in grafo.dic:
		arbol.AgregarVertice(x)
	while len(heap) > 0:
		a = heapq.heappop(heap)
		if a[2] in visitado:
			continue
		arista2 = (a[1],a[2],a[0])
		arbol.AgregarArista(arista2)
		visitado.append(a[2])
		for u in grafo.VerVecinos(a[2]):
			arista3 = (grafo.VerPeso(a[2],u),a[2],u)
			heapq.heappush(heap,arista3)
	return arbol

def armar_archivo1(archivo,camino,coordenadas):
	file = open(archivo,'w')

	file.write("%s\n" % ('<?xml version="1.0" encoding="UTF-8"?>'))
	file.write("%s\n" % ('<kml xmlns="http://earth.google.com/kml/2.1">'))
	file.write("\t%s\n" % ('<Document>'))
	file.write("\t\t%s\n\n" % ('<name>camino</name>'))
	for i in range(0,len(camino[0])):
		x = camino[0][i]
		coord1 = coordenadas[x]
		file.write("\t\t%s\n" % ('<Placemark>'))
		file.write("\t\t\t%s%s%s\n" % ('<name>',x, '</name>'))
		file.write("\t\t\t%s\n" % ('<Point>'))
		file.write("\t\t\t\t%s%s%s%s%s\n" % (' <coordinates>',str(coord1[0]),', ', str(coord1[1]),'</coordinates>'))
		file.write("\t\t\t%s\n" % ('</Point>'))
		file.write("\t\t%s\n\n" % ('</Placemark>'))

	for i in range(0,len(camino[0])):
		x = camino[0][i]
		coord1 = coordenadas[x]
		if i < len(camino[0])-1:
			y = camino[0][i+1]
			coord2 = coordenadas[y]
			file.write("\t\t%s\n" % ('<Placemark>'))
			file.write("\t\t\t%s\n" % ('<LineString>'))
			file.write("\t\t\t\t%s%s%s%s%s%s%s%s%s\n" % ('<coordinates>',str(coord1[0]),', ', str(coord1[1]),' ',str(coord2[0]),', ', str(coord2[1]),'</coordinates>'))
			file.write("\t\t\t%s\n" % ('</LineString>'))
			file.write("\t\t%s\n\n" % ('</Placemark>'))

	file.write("\t%s\n" % ('</Document>'))
	file.write("%s\n" % ('</kml>'))			
	file.close()

def armar_archivo2(archivo,camino,coordenadas):
	file = open(archivo,'w')

	file.write("%s\n" % ('<?xml version="1.0" encoding="UTF-8"?>'))
	file.write("%s\n" % ('<kml xmlns="http://earth.google.com/kml/2.1">'))
	file.write("\t%s\n" % ('<Document>'))
	file.write("\t\t%s\n\n" % ('<name>itinerario</name>'))
	for i in range(0,len(camino)):
		x = camino[i]
		coord1 = coordenadas[x]
		file.write("\t\t%s\n" % ('<Placemark>'))
		file.write("\t\t\t%s%s%s\n" % ('<name>',x, '</name>'))
		file.write("\t\t\t%s\n" % ('<Point>'))
		file.write("\t\t\t\t%s%s%s%s%s\n" % (' <coordinates>',str(coord1[0]),', ', str(coord1[1]),'</coordinates>'))
		file.write("\t\t\t%s\n" % ('</Point>'))
		file.write("\t\t%s\n\n" % ('</Placemark>'))

	for i in range(0,len(camino)):
		x = camino[i]
		coord1 = coordenadas[x]
		if i < len(camino)-1:
			y = camino[i+1]
			coord2 = coordenadas[y]
			file.write("\t\t%s\n" % ('<Placemark>'))
			file.write("\t\t\t%s\n" % ('<LineString>'))
			file.write("\t\t\t\t%s%s%s%s%s%s%s%s%s\n" % ('<coordinates>',str(coord1[0]),', ', str(coord1[1]),' ',str(coord2[0]),', ', str(coord2[1]),'</coordinates>'))
			file.write("\t\t\t%s\n" % ('</LineString>'))
			file.write("\t\t%s\n\n" % ('</Placemark>'))

	file.write("\t%s\n" % ('</Document>'))
	file.write("%s\n" % ('</kml>'))			
	file.close()

def abrir_archivo(file,coordenadas,grafoPesado,grafoDirigido):
	if os.path.isfile(file) == True:

		archivo = open(file, 'r')
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
