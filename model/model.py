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
