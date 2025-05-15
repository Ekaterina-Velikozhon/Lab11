import flet as ft

from UI.view import View
from database.DAO import DAO
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

        #aggiunto da me
        self._prodottoSelezionato = None

    def fillDD(self):
        colors = DAO.getAllColors()

        for color in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(text=color))

        for year in range(2015, 2019):
            self._view._ddyear.options.append(ft.dropdown.Option(text=str(year)))

        self._view.update_page()

    def handle_graph(self, e):
        if self._view._ddcolor.value is None or self._view._ddyear.value is None:
            self._view.create_alert("Manca qualche dato!")
            return

        self._model.buildGraph(self._view._ddcolor.value, self._view._ddyear.value)
        self.fillDDProduct()

        self._view._ddnode.disabled = False
        self._view.btn_search.disabled = False

        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodes()} Numero di archi: {self._model.getNumEdges()}"))

        #ДОПИСАТЬ ЧАСТЬ ПРО ARCHI CON PESI MAGGIORI
        freq = {}
        for e in self._model.getArchiPesoDecresente()[0:3]:
            self._view.txtOut.controls.append(
                ft.Text(f"Arco da {e[0].Product_number} a {e[1].Product_number}, peso={e[2]['weight']}"))
            if e[0].Product_number not in freq:
                freq[e[0].Product_number] = 1
            else:
                freq[e[0].Product_number] += 1

            if e[1].Product_number not in freq:
                freq[e[1].Product_number] = 1
            else:
                freq[e[1].Product_number] += 1

        n_repeated = []
        for k, v in freq.items():
            if v > 1:
                n_repeated.append(k)
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {n_repeated}"))

        self._view.update_page()



    def fillDDProduct(self):
        products = self._model.getNodes()

        self._view._ddnode.options.clear()
        for p in products:
            self._view._ddnode.options.append(ft.dropdown.Option(text=p.Product_number,
                                                                 data=p,  # associa l'oggetto all'opzione
                                                                 on_click=self.readDD))

    def readDD(self, e):
        self._prodottoSelezionato = e.control.data

    def handle_search(self, e):
        lunBest = self._model.trovaPercorso(self._prodottoSelezionato)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {lunBest}"))
        self._view.update_page()
