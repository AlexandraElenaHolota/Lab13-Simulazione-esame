import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        self.anno = None


    def fillDD(self):
        anno = [x for x in range(1910, 2015)]
        for a in anno:
            self._view.ddyear.options.append(
                ft.dropdown.Option(data=a,
                                   text=a,
                                   on_click=self.getSelectedAnno)
            )
        self._view.update_page()
    def getSelectedAnno(self, e):
        if e.control.data == None:
            self.anno = None
        else:
            self.anno = e.control.data
            self.fillddShape()
            self._view.update_page()

    def fillddShape(self):
        if self.anno != None:
            shape = self._model.getAllShape(self.anno)
            for s in shape:
                self._view.ddshape.options.append(ft.dropdown.Option(s))
            self._view.update_page()



    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        if self.anno is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un anno"))
            self._view.update_page()
            return
        if self._view.ddshape.value is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona una forma"))
            self._view.update_page()
            return

        self._grafo = self._model.buildGrafo(self.anno, self._view.ddshape.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(
            f"Il grafo è costituito di {n} nodi e {a} archi."))

        lista = self._model.printGrafo()
        for l in lista:
            self._view.txt_result.controls.append(ft.Text(l))
        self._view.update_page()



    def handle_path(self, e):
        self._model.percorsoMassimo()

        self._view.txtOut2.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.bestDistance)}"))

        for ii in self._model.edgesPath:
            self._view.txtOut2.controls.append(ft.Text(
                f"{ii[0]} --> {ii[1]}: weight {ii[2]} distance {str(self._model.distanza(ii))}"))  # ii[2]

        self._view.update_page()