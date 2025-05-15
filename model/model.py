import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

        #Esercizio2
        self._solBest = []
        self._lunBest = 0

    def getAllColors(self):
        colors = DAO.getAllColors()
        return colors

    def buildGraph(self, color, year):
        """Attenta, non posso fare la query che ho fatto prima perchè cosi prendo TUTTI i prodotti, anche se non sono presenti nel mio grafo"""
        products = DAO.getAllProducts(color)
        self._idMap = {}
        for p in products:
            self._idMap[p.Product_number] = p

        self._graph.clear()
        self._graph.add_nodes_from(products)

        for n1 in products:
            for n2 in products:
                if n1 != n2:
                    count = DAO.getSales(n1, n2, year)
                    if count[0] > 0:
                        self._graph.add_edge(n1, n2, weight=count[0])

    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNodes(self):
        return self._graph.nodes

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def getArchiPesoDecresente(self):
        return sorted(self._graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)


    #Esercizio2
    def trovaPercorso(self, source):
        self._solBest = []
        self._lunBest = 0

        parziale = []
        self._ricorsione(parziale, source, 0)
        return len(self._solBest)

    def _ricorsione(self, parziale, nodoLast, livello):
        archiViciniAmmissibili = self._archiAmmissibili(parziale, nodoLast)

        if len(archiViciniAmmissibili) == 0:
            if len(parziale) > self._lunBest:
                self._lunBest = len(parziale)
                self._solBest = copy.deepcopy(parziale)
        else:
            for a in archiViciniAmmissibili:
                parziale.append(a)
                self._ricorsione(parziale, a[1], livello + 1)
                parziale.pop()

    def _archiAmmissibili(self, parziale, nodoLast):
        archi = self._graph.edges(nodoLast, data=True)

        result= []

        for a in archi:
            if self._verificaPeso(a, parziale) and self._isNuovo(a, parziale):
                result.append(a)
        return result

    def _isNuovo(self, arco, parziale):
        if len(parziale) == 0:
            return True

        arco_inverso = (arco[1], arco[0], arco[2])
        if arco_inverso not in parziale and arco not in parziale:
            return True
        else:
            return False

    def _verificaPeso(self, arco, parziale):
        if len(parziale) == 0:
            return True

        if arco[2]["weight"] >= parziale[-1][2]["weight"]:
            return True
        else:
            return False
