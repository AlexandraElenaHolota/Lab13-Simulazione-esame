import networkx as nx
from geopy import distance

from database.DAO import DAO
class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}
        self.nodes = None
        self.edges = None
        self.edgesPath = []
        self.nodiPath = []
        self.bestDistance = 0

    def percorsoMassimo(self):
        self.edgesPath = []
        self.nodiPath = []
        self.bestDistance = 0

        for n in self.idMap.keys():
            parziale = []
            parziale.append(n)
            self.ricorsione(parziale, [])

    def ricorsione(self, parziale, p_edges):
        ultimo = parziale[-1]

        vicini = self.viciniOk(ultimo, p_edges)

        if len(vicini) == 0:
            peso = self.calcolaPeso(p_edges)
            if peso > self.bestDistance:
                self.bestDistance = peso+0.0
                self.nodiPath = parziale[:]
                self.edgesPath = p_edges[:]
            return

        for v in vicini:
            p_edges.append((ultimo, v, self.grafo.get_edge_data(ultimo, v)['weight']))
            parziale.append(v)

            self.ricorsione(parziale, p_edges)
            parziale.pop()
            p_edges.pop()

    def calcolaPeso(self, p_edges):
        peso = 0
        for v in p_edges:
            peso += distance.geodesic((self.idMap[v[0]].Lat, self.idMap[v[0]].Lng), (self.idMap[v[1]].Lat,self.idMap[v[1]].Lng)).km
        return peso


    def viciniOk(self, ultimo, p_edges):
        vicini = self.grafo.edges(ultimo, data=True)

        risultati = []
        for edge in vicini:
            if len(p_edges)!=0:
                if edge[2]["weight"] > p_edges[-1][2]:
                    risultati.append(edge[1])
            else:
                risultati.append(edge[1])
        return risultati

    def distanza(self, v):
        return distance.geodesic((self.idMap[v[0]].Lat, self.idMap[v[0]].Lng), (self.idMap[v[1]].Lat,self.idMap[v[1]].Lng)).km









    def buildGrafo(self, anno, shape):
        self.grafo.clear()
        #aggiungi nodi
        self.nodes = DAO.getAllState()
        self.idMap = {n.id: n for n in self.nodes}
        self.grafo.add_nodes_from(self.idMap.keys())

        #aggiungi archi pesati
        self.edges = DAO.getAllWeightEdges(anno, shape)
        for edge in self.edges:
            self.grafo.add_edge(edge[0], edge[1], weight=edge[2])

    def printGraph(self):
        print(f"nodi: {len(self.grafo.nodes)}, archi: {len(self.grafo.edges)}")

    def printGrafo(self):
        lista = []
        for nod in self.idMap.keys():
            vicini = self.grafo.neighbors(nod)
            somma = 0
            for v in vicini:
                somma += self.grafo[nod][v]['weight']
            lista.append(f"Nodo {nod}. Somma pesi su archi {somma}")
        return lista

    def getGraphDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def getAllShape(self,anno):
        return DAO.getAllShape(anno)