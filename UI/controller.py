import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        year=self._view._ddAnno.value
        if year is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"seleziona anno"))
            self._view.update_page()
            return

        self._model.buildGraph(int(year))
        nNodes,nEdges = self._model.getGraphDetails()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"grafo correttamente creato"))
        self._view._txt_result.controls.append(ft.Text(f"num nodi: {nNodes}; num edges: {nEdges}"))
        self._view.update_page()


    def handleDettagli(self, e):
        if self._squadraScelta is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(value="Per favore selezionare un team.", color="red"))
            self._view.update_page()
            return

        #[(VO,PO),(V1,P1)
        viciniSorted= self._model.getNeighborsSorted(self._squadraScelta)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Il vicinato conta {len(viciniSorted)} squadre.")
        )
        for v in viciniSorted:
            self._view._txt_result.controls.append(
                ft.Text(f"{v[0]} -- peso: {v[1]}")
            )
        self._view.update_page()

    def handlePercorso(self, e):
        if self._squadraScelta is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(value="Per favore seleziona un team.", color="red"))
            self._view.update_page()
            return
        path,score = self._model.getBestPathV2(self._squadraScelta)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"cammino che parte da {self._squadraScelta} -- peso: {score}"))
        self._view.update_page()
        for v in path:
            self._view._txt_result.controls.append(ft.Text(f"{v}"))
        self._view.update_page()




    def fillDDanno(self):
        #lo chiamo in view sotto al dd
        listaAnni= self._model.getYears()
        for year in listaAnni:
            self._view._ddAnno.options.append(ft.dropdown.Option(year))

    def changeAnno(self,e):
        #on_change=self._controller.changeAnno MESSO IN VIEW
        anno= self._view._ddAnno.value
        squadre=self._model.getTeamsOfYear(anno)#fai i controlli!! come a lab 11
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(squadre)} squadre che hanno giocato nell'anno {anno}:"))
        for squadra in squadre:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{squadra}"))
        self._view.update_page()

        #adesso posso aggiornare tendina squadre
        self.fillDDSquadre(squadre)
        self._view.update_page()

    def fillDDSquadre(self, squadre):
        for squadra in squadre:  # sto appendendo al dropdown l'oggetto reatiler
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(key=squadra.ID,  # 🔑 Chiave univoca dell'opzione
                                   text=squadra.name,  # 🏷️ Testo visibile nel menu a tendina
                                   data=squadra,
                                   # 📦 Oggetto completo, utile per accedere a tutti gli attributi dopo la selezione
                                   on_click=self.read_squadra))  # salvati l'oggetto da qualche parte

    def read_squadra(self, e):
        self._squadraScelta = e.control.data  # l'abbiamo inizializzata a None
        # e.control.data è il risultato di onclick sopra
