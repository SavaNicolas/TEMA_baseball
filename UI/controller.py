import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self, e):
        pass

    def handlePercorso(self, e):
        pass

    def fillDDanno(self):
        listaAnni= self._model.getYears()
        for year in listaAnni:
            self._view._ddAnno.options.append(ft.dropdown.Option(year))

    def changeAnno(self,e):
        anno= self._view._ddAnno.value
        squadre=self._model.getTeamsOfYear(anno)
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