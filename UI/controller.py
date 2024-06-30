import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(str(i)))
        self._view.update_page()
        self._listCountry = self._model.getCountries()
        for n in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(str(n)))
        self._view.update_page()



    def handle_graph(self, e):
        selected_year = self._view.ddyear.value
        selected_county = self._view.ddcountry.value
        if selected_year is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci un Anno!", color='red'))
            self._view.update_page()
        if selected_county is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci una Nazione!", color='red'))
            self._view.update_page()
        else:
            try:
                selected_year = int(selected_year)
            except ValueError:
                self._view.txt_result.controls.append(ft.Text("Inserisci un Anno valido!", color='red'))
                self._view.update_page()

            self._model.buildGraph2(selected_year, selected_county)
            self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
            self._view.txt_result.controls.append(ft.Text(f"Grafo con {len(self._model.grafo.nodes)} nodi e {len(self._model.grafo.edges)} archi"))
            self._view.update_page()



    def handle_volume(self, e):
        if self._model.grafo:
            vol = self._model.getVolumi()
            for k,v in vol.items():
                self._view.txtOut2 .controls.append(ft.Text(f"{k}--->{v}"))
                self._view.update_page()
        else:
            self._view.txtOut2.controls.append(ft.Text("Creare un Grafo", color = "red"))
            self._view.update_page()


    def handle_path(self, e):
        soglia = self._view.txtN.value
        if soglia is None:
            self._view.txtOut3.controls.append(ft.Text("Inserisci un numero di archi!", color='red'))
            self._view.update_page()
        else:
            try:
                soglia = int(soglia)
            except ValueError:
                self._view.txt_result.controls.append(ft.Text("Inserisci una soglia intera!", color='red'))
                self._view.update_page()

            if soglia < 2:
                self._view.txt_result.controls.append(ft.Text("Inserisci una soglia del valore di almeno 2", color='red'))
                self._view.update_page()
            else:
                percorso = self._model.getPath(soglia)
                self._view.txt_result.controls.append(
                    ft.Text(f"La somma totale dei pesi degli archi per il cammino trovato è: {percorso[1]}"))
                self._view.update_page()
                for i in range(0, len(percorso[0])-1):
                    self._view.txt_result.controls.append(
                        ft.Text(f"{percorso[0][i].Retailer_name} -> {percorso[0][i+1].Retailer_name}: {self._model.grafo[percorso[0][i]][percorso[0][i+1]]["weight"]}"))
                    self._view.update_page()
