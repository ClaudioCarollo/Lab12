import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._bestComp = None
        self._bestdTot = None
        self.grafo = nx.Graph()
        self.idmap = {}

    def getCountries(self):
        nazioni = DAO.getCountries()
        return nazioni

    def buildGraph(self, year, country):
        self.grafo.clear()
        nodi = DAO.getRetailers(country)
        self.grafo.add_nodes_from(nodi)
        for n in self.grafo.nodes:
            self.idmap[n.Retailer_code] = n
        connessioni = DAO.getAllConnessioni(year, country, self.idmap)
        for c in connessioni:
            self.grafo.add_edge(c.retailer1, c.retailer2, weight=c.peso)

    def buildGraph2(self, year, country):
        self.grafo.clear()
        nodi = DAO.getRetailers(country)
        self.grafo.add_nodes_from(nodi)
        for n in self.grafo.nodes:
            self.idmap[n.Retailer_code] = n
        for n1 in self.grafo.nodes:
            for n2 in self.grafo.nodes:
                if n1 != n2:
                    peso = DAO.getAllConnessioni2(n1.Retailer_code, n2.Retailer_code, year, country)
                    if peso>0:
                        self.grafo.add_edge(n1, n2, weight=peso)

    def getVolumi(self):
        volumi = {}
        for n1 in self.grafo.nodes:
            peso_incidente = 0
            for n2 in self.grafo.neighbors(n1):
                peso_incidente += self.grafo[n1][n2]["weight"]
            volumi[n1.Retailer_name] = peso_incidente
        #ordina un dizionario per valore decrescente
        volumi_ordinati = dict(sorted(volumi.items(), key=lambda x: x[1], reverse=True))
        return volumi_ordinati

    def getPath(self, N):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = []
        for a in self.grafo.nodes:
            if a not in parziale and len(parziale)-1 < N:
                parziale.append(a)
                self._ricorsionev2(parziale, N)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
        return self._bestComp, self._bestdTot

    def _ricorsionev2(self, parziale, N):
        # verifico se soluzione è migliore di quella salvata in cache
        if len(parziale) == N:
            if self.grafo.has_edge(parziale[-1],parziale[0]):
                parziale.append(parziale[0])
            if self._getScore(parziale) > self._bestdTot:
                # se lo è aggiorno i valori migliori
                self._bestComp = copy.deepcopy(parziale)
                self._bestdTot = self._getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        comp = nx.node_connected_component(self.grafo, parziale[-1])
        for a in comp:
            if a not in parziale and len(parziale)-1 < N:
                parziale.append(a)
                self._ricorsionev2(parziale, N)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking

    def _getScore(self, listOfNodes):
        score = 0
        for i in range(0, len(listOfNodes)-1):
            score += self.grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return score