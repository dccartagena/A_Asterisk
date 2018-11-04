__author__ = 'dccartagena'
#1: obstaculo
#2: robot
#3: meta

from Nodo import nodo
import time
import random
import math
import numpy as np

random.seed()

#Funcion para localizar el robot en el mapa
def searchrobot(mapa):
    for i in range(len(mapa)):
        for k in range(len(mapa[0])):
            if (mapa[i][k] == 2):
                pos = [i, k]
    return pos

#Operadores de movimiento
def movright(map):
    newmap = [x[:] for x in map]
    pos = searchrobot(map)
    node = nodo(newmap)
    if (pos[1] + 1 < len(map[0])):
        newpos = [pos[0], pos[1] + 1]
        if (newmap[newpos[0]][newpos[1]] == 0):
            newmap[newpos[0]][newpos[1]] = 2
            newmap[pos[0]][pos[1]] = 0
            if newmap != map:
                node.map = newmap
                node.pos = newpos
                return node
            else:
                return None
    else:
        return None

def movleft(map):
    newmap = [x[:] for x in map]
    pos = searchrobot(map)
    node = nodo(newmap)
    if (pos[1] - 1 >= 0):
        newpos = [pos[0], (pos[1] - 1)]
        if (newmap[newpos[0]][newpos[1]] == 0):
            newmap[newpos[0]][newpos[1]] = 2
            newmap[pos[0]][pos[1]] = 0
            if newmap != map:
                node.map = newmap
                node.pos = newpos
                return node
            else:
                return None
    else:
        return None

def movdown(map):
    newmap = [x[:] for x in map]
    pos = searchrobot(map)
    node = nodo(newmap)
    if ((pos[0] + 1 )< len(map)):
        newpos = [(pos[0] + 1), pos[1]]
        if (newmap[newpos[0]][newpos[1]] == 0):
            newmap[newpos[0]][newpos[1]] = 2
            newmap[pos[0]][pos[1]] = 0
            if newmap != map:
                node.map = newmap
                node.pos = newpos
                return node
            else:
                return None
    else:
        return None

def movup(map):
    newmap = [x[:] for x in map]
    pos = searchrobot(map)
    node = nodo(newmap)
    if pos[0] - 1 >= 0:
        newpos = [(pos[0] - 1), (pos[1])]
        if (newmap[newpos[0]][newpos[1]] == 0):
            newmap[newpos[0]][newpos[1]] = 2
            newmap[pos[0]][pos[1]] = 0
            if newmap != map:
                node.map = newmap
                node.pos = newpos
                return node
            else:
                return None
    else:
        return None

#Funcion para revisar si se llego a la solucion
def checksol(solucion, node):
    issol = False
    for i in range(len(solucion)):
        if (node.map == solucion[i]):
            issol = True
    return issol

#Funcion para generar nodos hijos
def childgen(node):
    nodohijo = [None]*4
    nodohijo[0] = movright(node.map)
    nodohijo[1] = movleft(node.map)
    nodohijo[2] = movup(node.map)
    nodohijo[3] = movdown(node.map)
    return nodohijo

#Funcion de busqueda a lo ancho
def busquedaancho(init, solucion):
    start = time.clock()
    root = nodo(init)
    tree = []
    tree.append(root)
    issolved = False
    listedtree = []
    while (not issolved) and (len(tree) > 0):
        node = tree.pop(0)
        listedtree.append(node)
        if checksol(solucion, node):
            end = time.clock() - start
            print('Tiempo en busqueda a lo ancho ' + str(end))
            return node
        else:
            nodohijo = childgen(node)
            for i in range(len(nodohijo)):
                if nodohijo[i] is not None:
                    if (not nodohijo[i].islisted(listedtree)) and (not nodohijo[i].islisted(tree)):
                        tree.append(nodohijo[i])
                        node.addchild(nodohijo[i])

#Funciones de algoritmo genetico
def isinvector(list, vector):
    flag = 0
    for i in list:
        if i != None:
            if vector == i:
              flag = 1
    return flag

#Generacion de poblacion
def genpoblacion(vector):
    cantind = 10
    poblacion = [None]*cantind
    od = [0, 1, 2, 3]
    k = 0
    for i in range(cantind)*5:
        random.shuffle(od)
        prop = [vector[od[0]], vector[od[1]], vector[od[2]], vector[od[3]]]
        if isinvector(poblacion, prop) != 1:
            poblacion[k] = prop
            k += 1
        if k >= cantind:
            break
    return poblacion

#Funcion de cruce entre individuos
def cruce(vector):
    hijo = [None]*2
    if (vector[0] != None) and (vector[1] != None):
        hijo[0] = [vector[0][0], vector[0][1], vector[1][2], vector[1][3]]
        hijo[1] = [vector[1][0], vector[1][1], vector[0][2], vector[0][3]]
        return hijo
    else:
        None

#Fucnion de mutacion
def mutacion(vector):
    newvector = [None]*2
    if (vector[0] != None) and (vector[1] != None):
        newvector[0] = [vector[0][3], vector[0][1], vector[0][2], vector[0][1]]
        newvector[1] = [vector[1][3], vector[1][1], vector[1][2], vector[1][1]]
        return newvector
    else:
        return None

#Funcion de seleccion de individuos
def seleccion(poblacion):
    ind = [None]*2
    for i in range(2):
        sel = random.randint(0, 9)
        ind[i] = poblacion[sel]
    return ind

#Funcion para indicar el mejor individuo
def best_ind(lista):
    best_value = 0
    best_i = 0
    for i in range(len(lista)):
        if lista[i] != None:
            if lista[i][0] != None:
                if lista[i][0].value > best_value:
                    best_i = i
    if lista[best_i] != None:
        return lista[best_i]
    else:
        return None

#Base del Algoritmo genetico
def genetico(vector):
    for i in range(50):
        hijo = [None]*2
        probmuta = random.random()
        probcruz = random.random()
        poblacion = genpoblacion(vector)
        individuos = seleccion(poblacion)
        if probcruz < 0.9:
            pre = cruce(individuos)
            if pre != None:
                individuos = pre
        if probmuta < 0.3:
            pre = mutacion(individuos)
            if pre != None:
                individuos = pre
        if individuos != None:
            mejor_ind = best_ind(individuos)
        if mejor_ind != None:
            break
    return mejor_ind

#Busqueda basada en el algoritmo genetico
def busquedaheurgenetica(init, solucion):
    start = time.clock()
    root = nodo(init)
    root.pos = searchrobot(root.map)
    tree = [root]
    issolved = False
    listedtree = []
    profundidad = 0
    while (not issolved) and (len(tree) > 0):
        node = tree.pop()
        listedtree.append(node)
        if checksol(solucion, node):
            end = time.clock() - start
            print('Tiempo en usando heuristica con algoritmo genetico' + str(end))
            return node
        else:
            nodohijo = childgen(node)
            nodohijo = setvalue(nodohijo, root)
            k = 100
            for i in range(k):
                nodosel = genetico(nodohijo)
                if nodosel != None:
                    for i in range(len(nodosel)):
                        if nodosel[i] != None:
                            if (not nodosel[i].islisted(listedtree)) and (not nodosel[i].islisted(tree)):
                                tree.append(nodosel[i])
                                node.addchild(nodosel[i])
                                node.prof = profundidad
                                profundidad += 1
                                break

#Funciones para busqueda heuristica
def setvalue(hijos, root):
#convencion Last_move:
# 0 = derecha
# 1 = izquierda
# 2 = arriba
# 3 = abajo
    for i in range(len(hijos)):
        if hijos[i] != None:
            hijos[i].value = cercania(hijos[i], root)
    return hijos

#Funcion para aplicar la heuristica
def cercania(node, root):
    #Se revisa cercania con el origen
    distO = math.sqrt(math.pow((node.pos[0] - root.pos[0]), 2) + math.pow((node.pos[1] - root.pos[1]), 2))
    return distO

#Busqueda A asterisco
def busquedaheuristica(init, solucion):
    start = time.clock()
    root = nodo(init)
    root.pos = searchrobot(root.map)
    tree = [root]
    issolved = False
    listedtree = []
    profundidad = 0
    while (not issolved) and (len(tree) > 0):
        node = tree.pop()
        listedtree.append(node)
        if checksol(solucion, node):
            end = time.clock() - start
            print('Tiempo en usando heuristica' + str(end))
            return node
        else:
            nodohijo = childgen(node)
            nodohijo = setvalue(nodohijo, root)
            best_value = -1
            if nodohijo != None:
                for i in range(len(nodohijo)):
                    if nodohijo[i] != None:
                        if nodohijo[i].value > best_value:
                            best_value = nodohijo[i].value + nodohijo[i].prof
                            besti = i
                            if (not nodohijo[besti].islisted(listedtree)) and (not nodohijo[besti].islisted(tree)):
                                tree.append(nodohijo[besti])
                                node.addchild(nodohijo[besti])
                                node.prof = profundidad
                                profundidad += 1

#Busqueda a lo largo
def busquedalargo(init, solucion):
    start = time.clock()
    root = nodo(init)
    root.pos = searchrobot(root.map)
    tree = [root]
    issolved = False
    listedtree = []
    profundidad = 0
    while (not issolved) and (len(tree) > 0):
        node = tree.pop()
        listedtree.append(node)
        if checksol(solucion, node):
            end = time.clock() - start
            print('Tiempo en usando busqueda a lo largo' + str(end))
            return node
        else:
            nodohijo = childgen(node)
            best_value = 1000
            if nodohijo != None:
                for i in range(len(nodohijo)):
                    if nodohijo[i] != None:
                        if nodohijo[i].value < best_value:
                            best_value = nodohijo[i].prof
                            besti = i
                            if (not nodohijo[besti].islisted(listedtree)) and (not nodohijo[besti].islisted(tree)):
                                tree.append(nodohijo[besti])
                                node.addchild(nodohijo[besti])
                                node.prof = profundidad
                                profundidad += 1

#------------Funcion para generar posibles soluciones-----------
def gensol(init):
    m = 0
    pos = searchrobot(init)
    mapa = []
    for i in range(len(init)):
        for k in range(len(init[0])):
            if init[i][k] == 3:
                if i - 1 >= 0:
                    if init[i - 1][k] == 0:
                        mapa1 = [x[:] for x in init]
                        mapa1[pos[0]][pos[1]] = 0
                        mapa.append(mapa1)
                        mapa[m][i - 1][k] = 2
                        m += 1
                if i + 1 < len(init):
                    if init[i + 1][k] == 0:
                        mapa1 = [x[:] for x in init]
                        mapa1[pos[0]][pos[1]] = 0
                        mapa.append(mapa1)
                        mapa[m][i + 1][k] = 2
                        m += 1
                if k - 1 >= 0:
                    if init[i][k - 1] == 0:
                        mapa1 = [x[:] for x in init]
                        mapa1[pos[0]][pos[1]] = 0
                        mapa.append(mapa1)
                        mapa[m][i][k - 1] = 2
                        m += 1
                if k + 1 < len(init[0]):
                    if init[i][k + 1] == 0:
                        mapa1 = [x[:] for x in init]
                        mapa1[pos[0]][pos[1]] = 0
                        mapa.append(mapa1)
                        mapa[m][i][k + 1] = 2
                        m += 1
    return mapa

# ---------Funcion para imprimir mapas----------
def printresult(nodesol, init):
    camino = []
    map1 = [x[:] for x in init]
    if nodesol is not None:
        print("Nodos recorridos:" + str(nodesol.prof))
        while nodesol.parent is not None:
            camino.append(nodesol.pos)
            nodesol = nodesol.parent
        for i in range(len(camino)):
            map1[camino[i][0]][camino[i][1]] = 2
        #camino.reverse()
        """
        for i in range(len(map1)):
            print str(map1[i])
        """
        return map1
    else:
        print('No se encontro solucion')


def main():

    #Estado inicial del mapa

    init = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 1]]

    posi = searchrobot(init) #Posicion inicial del robot, se recomienda [0,0]

    #Generacion de soluciones
    sol = gensol(init)

    nodesol1 = busquedaancho(init, sol)
    solucion = printresult(nodesol1, init)

    #nodesol2 = busquedalargo(init, solucion)
    #printresult(nodesol2, init)

    #nodesol3 = busquedaheuristica(init, solucion)
    #printresult(nodesol3, init)

    #nodesol4 = busquedaheurgenetica(init, solucion)
    #printresult(nodesol4, init)

main()