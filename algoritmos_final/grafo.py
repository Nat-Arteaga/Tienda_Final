# Grafo

import heapq

class Grafo:
    def __init__(self):
        self.grafo = {}

    def agregar_arista(self, origen, destino, peso):
        if origen not in self.grafo:
            self.grafo[origen] = {}
        if destino not in self.grafo:
            self.grafo[destino] = {}


        self.grafo[origen][destino] = peso
        self.grafo[destino][origen] = peso

    def dijkstra(self, inicio, fin):
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0
        camino = {nodo: None for nodo in self.grafo}
        cola_prioridad = [(0, inicio)]

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
            if distancia_actual > distancias[nodo_actual]:
                continue
            for vecino, peso in self.grafo.get(nodo_actual, {}).items():
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    camino[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

        ruta = []
        actual = fin
        while actual is not None:
            ruta.append(actual)
            if actual == inicio:
                break
            actual = camino[actual]

        if len(ruta) == 1 and ruta[0] == fin and fin != inicio:
            return [], float('inf')
        return ruta[::-1], distancias[fin]