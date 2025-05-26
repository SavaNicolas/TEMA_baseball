import copy
import warnings

import networkx as nx

from database.DAO import DAO


class Model:

    #grafooooo
    def __init__(self):
        self.squadre= []
        self._productsAll = DAO.getAllTeams()  # lista con tutte le squadre, per avere l'id map
        # creo grafo
        self._grafo = nx.Graph()
        # mappa di oggetti
        self.idMapTeams= {}
        for p in self._productsAll:
            self.idMapTeams[p.ID] = p

        self._bestPath=[]
        self._bestScore=0

    def getBestPathV2(self,start):
        self._bestPath = []
        self._bestScore = 0
        parziale= [start]

        vicini= self._grafo.neighbors(start)
        #siccome il primo metodo è troppo lungo, allora sorto la lista dei vicini e prendo quello con peso più grnde senza iterare
        viciniTuples = [(v, self._grafo[start][v]["weight"]) for v in vicini]
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        # for v in vicini:
        parziale.append(viciniTuples[0][0])#è il nodo stesso. ci fosse stato [1] alla fine sarebbe stato il peso
        self.ricorsioneV2(parziale)
        # parziale.pop() non mi serve più perchè non sto iterando

        return self.getWeightsOfPath(self,self._bestPath ), self._bestScore

    def ricorsioneV2(self,parziale):
        # Verifico che parziale sia una soluzione, e verifico se migliore della best
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)

        #verifico se posso aggiungere un nuovo nodo
            #non deve essere in parziale il vicino dell'ultimo nodo aggiunto
        vicini = self._grafo.neighbors(parziale[-1])
        viciniTuples = [(v, self._grafo[parziale[-1]][v]["weight"]) for v in vicini]
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        for t in viciniTuples:
            if (t[0] not in parziale and
                    self._grafo[parziale[-2]][parziale[-1]]["weight"] > t[1]):
                parziale.append(t[0])
                self.ricorsione(parziale)
                parziale.pop()
                return #importante perchè io mozzo la ricorsione prendendo il nodo che mi interessa

        #aggiungo nodo e faccio ricorsione


    def getBestPath(self,start):
        self._bestPath = []
        self._bestScore = 0
        parziale= [start]

        vicini= self._grafo.neighbors(start)
        for v in vicini:
            parziale.append(v)#questo per partire sempre da una situa in cui parziale ha 2 oggetti
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestScore

    def ricorsione(self,parziale):
        # Verifico che parziale sia una soluzione, e verifico se migliore della best
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)

        #verifico se posso aggiungere un nuovo nodo
            #non deve essere in parziale il vicino dell'ultimo nodo aggiunto
        for v in self._grafo.neighbors(parziale[-1]):
            if (v not in parziale and
                    self._grafo[parziale[-2]][parziale[-1]]["weight"] > self._grafo[parziale[-1]][v]["weight"]):
                parziale.append(v)
                self.ricorsione(parziale)
                parziale.pop()

        #aggiungo nodo e faccio ricorsione

    def score(self, listOfNodes):
        if len(listOfNodes) < 2:
            warnings.warn("Errore in score, attesa lista lunga almeno 2.")

        totPeso = 0
        for i in range(len(listOfNodes) - 1):
            totPeso += self._grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return totPeso

    def buildGraph(self,year):
        self._grafo.clear()#va pulito
        #i nodi sono le squadre che abbiamo selezionato al punto precedente
        # aggiungiamo i nodi
        self._grafo.add_nodes_from(self.squadre)
        # aggiungo archi
        self.addEdges(year)

    def addEdges(self,year):
        for u in self.squadre:  # prendo nodo1
            for v in self.squadre:  # prendo nodo2
                if u != v:
                    self._grafo.add_edge(u, v)
                    listaU= DAO.salaryOfTeams(year,u.ID,self.idMapTeams) #[(squadra,peso)]
                    listaV=DAO.salaryOfTeams(year,v.ID,self.idMapTeams)
                    if len(listaU)>0 and len(listaV)>0:
                        peso= listaU[0][1]+listaV[0][1]
                        # Modifica del peso di un arco esistente
                        self._grafo[u][v]['weight'] = peso
                        print(f"aggiunto arco {u}-{v} con peso {peso}")

    #calcola somma dei salari di ciascuna squadra
    #Il peso di ciascun arco del grafo deve corrispondere alla somma dei salari dei giocatori delle due squadre(somma salari giocatori squadra 1+ somma squadra 2) nell’anno considerato.

    def getYears(self):
        return DAO.getYears()

    def getTeamsOfYear(self,anno):
        self.squadre= DAO.getTeamsOfYearAnno(anno)
        return self.squadre

    def getGraphDetails(self):
        return len(self._grafo.nodes()),len(self._grafo.edges())

    def getIdMapTeams(self):
        return self.idMapTeams

    def getNeighborsSorted(self,source):

        vicini = nx.neighbors(self._grafo,source) #lista di vicini

        viciniTuple= [] #lista tupla (vicino, peso arco)
        for v in vicini:
            viciniTuple.append((v,self._grafo[source][v]["weight"]))

        viciniTuple.sort(key=lambda x: x[1])
        return viciniTuple

    def getWeightsOfPath(self, path):
        pathTuple = [(path[0], 0)]
        for i in range(1, len(path)):
            pathTuple.append((path[i], self._grafo[path[i - 1]][path[i]]["weight"]))
        return pathTuple

