import lib
from grafoPeso import grafoPeso
from grafoDir import grafoDir


graph=grafoPeso({})
graph.AgregarVertice('A')
graph.AgregarVertice('B')
graph.AgregarVertice('C')
graph.AgregarVertice('D')
graph.AgregarVertice('E')
graph.AgregarArista(('A','B',1))
graph.AgregarArista(('B','C',4))
graph.AgregarArista(('A','D',2))
graph.AgregarArista(('B','D',3))
graph.AgregarArista(('D','C',2))
graph.AgregarArista(('C','E',2))
graph.AgregarArista(('E','D',703))
graph.AgregarArista(('E','B',7))
print('grafo pesado')
print(graph.dic)
print('\n')
print('viajante')
print(lib.viajante(graph,'A'))
print('\n')
print('camino minimo')
print(lib.camino_minimo(graph,'A','E'))
print('\n')
print('arbol tendido minimo')
arbol = lib.arbol_tendido_minimo(graph)
print(arbol.dic)
print('\n')
print('viajante aproximado')
print(lib.viajante_aproximado(graph,'A'))
print('\n')

graph2=grafoDir({})
graph2.AgregarVertice('A')
graph2.AgregarVertice('B')
graph2.AgregarVertice('C')
graph2.AgregarVertice('D')
graph2.AgregarVertice('E')
graph2.AgregarArista(('A','B'))
graph2.AgregarArista(('B','C'))
graph2.AgregarArista(('A','D'))
graph2.AgregarArista(('B','D'))
graph2.AgregarArista(('D','C'))
graph2.AgregarArista(('C','E'))
print('grafo dirigido')
print(graph2.dic)
print('\n')
print('orden topologico')
print(lib.orden_topologico(graph2))