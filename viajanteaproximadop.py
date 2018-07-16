def viajante_aproximado_funcion(grafo,origen):
	visitado = []
	padre = {}
	dist = {}
	cola = queue.Queue()
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

'''def viajante_aproximado_funcion(grafo,origen):
	visitado = []
	padre = {}
	dist = {}
	cola = queue.Queue()
	visitado.append(origen)
	heap = []
	padre[origen] = None
	dist[origen] = 0
	heapq.heappush(heap,origen)
	MinimoP = 0
	MinimoV = origen
	while len (heap) > 0:
		v = heapq.heappop(heap)
		contador = 0
		for w in grafo.VerVecinos(v):
			actualP = grafo.VerPeso(v,w)
			actualV = w
			for u in grafo.VerVecinos(v):
				siguienteP = grafo.VerPeso(v,u)
				siguienteV = u
				if w == u:
					continue
				if actual < siguiente:
					MinimoP = actualP
					MinimoV = actualV
				else:
					MinimoP = siguienteP
					MinimoV = siguienteV
		if MinimoV not in visitado:
			visitado.append(MinimoV)
			padre[MinimoV] = v
			dist[MinimoV] = dist[v] + MinimoP
			heapq.heappush(heap,MinimoV)
			break
		else:
			continue
	return padre,dist'''