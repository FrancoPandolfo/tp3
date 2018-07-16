import os.path
import sys
import lib
from grafoPeso import grafoPeso
from grafoDir import grafoDir

def main():
	grafoPesado = grafoPeso({})
	grafoDirigido = grafoDir({})

	if len(sys.argv) < 3:
		print('faltan parametros')
		sys.exit()

	else:
		coordenadas = {}
		lib.abrir_archivo(sys.argv[1],coordenadas,grafoPesado,grafoDirigido)
		for line in sys.stdin:

			text = line.rstrip()
			cadena = text.split(' ')
	
			if cadena[0] == 'ir':
				pos_coma = 0
				for i in range(1,len(cadena)):
					for j in range(0,len(cadena[i])):
						if cadena[i][j] == ',':
							pos_coma = i
							break
				cadena[pos_coma] = cadena[pos_coma][:-1]
				s1 = ' '
				actual1 = []
				if i > 1:
					for i in range(1,pos_coma+1):
						actual1.append(cadena[i])
					cadena[1] = s1.join(actual1)

				cont = 0
				for i in range(pos_coma+1,len(cadena)): 
					cont += 1
				s2 = ' '
				actual2 = []
				if cont > 1:
					for i in range(pos_coma+1,len(cadena)):
						actual2.append(cadena[i])
					cadena[2] = s2.join(actual2)

				camino = lib.camino_minimo(grafoPesado,cadena[1],cadena[2])
				print(' -> '.join(camino[0]))
				print('Costo total:', camino[1])
				archivo = sys.argv[2]
				lib.armar_archivo1(archivo,camino,coordenadas)

			if cadena[0] == 'viaje':
				cadena[1] = cadena[1][:-1]
				s = ' '
				actual = []
				if len(cadena) > 3:
					for i in range(2,len(cadena)):
						actual.append(cadena[i])
					cadena[2] = s.join(actual)

				if cadena[1] == 'optimo':
					camino = lib.viajante(grafoPesado,cadena[2])
					print(' -> '.join(camino[0]))
					print('Costo total:', camino[1])
					archivo = sys.argv[2]
					lib.armar_archivo1(archivo,camino,coordenadas)

				elif cadena[1] == 'aproximado':
					camino = lib.viajante_aproximado(grafoPesado,cadena[2])
					print(' -> '.join(camino[0]))
					print('Costo total:', camino[1])
					archivo = sys.argv[2]
					lib.armar_archivo1(archivo,camino,coordenadas)

				else:
					print('comando incorrecto')
					sys.exit()

			if cadena[0] == 'itinerario':
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
					print(' -> '.join(camino))
					archivo = sys.argv[2]
					lib.armar_archivo2(archivo,camino,coordenadas)
					


			if cadena[0] == 'reducir_caminos':
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

main()